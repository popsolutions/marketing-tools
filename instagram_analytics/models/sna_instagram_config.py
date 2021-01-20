# -*- coding: utf-8 -*-

import re
from odoo import models, fields, api
from datetime import datetime
from instagram_private_api import Client, ClientCompatPatch
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

class InstagramConfig(models.Model):
    _name = 'sna.instagram.config'

    name = fields.Char()
    username = fields.Char()
    password = fields.Char()

    @api.multi
    def _start_getting_posts(self, values):
        username = values['username']
        password = values['password']

        try:
            more = True

            api = Client(username, password)
            print(api)

            results = api.self_feed(count=50)

            while more:
                # Iterate trhough result items
                if 'items' in results:
                    for i in results['items']:
                        caption = '' if 'caption' in i and i['caption'] is None else i['caption']['text']

                        hashtags = set(part for part in caption.split() if part.startswith('#'))

                        hashtag_ids = []

                        for h in hashtags:
                            hashtag = self.sudo().env['sna.instagram.post.hashtag'].search([('name', '=', h)])
                            if len(hashtag) == 0:
                                hashtag = self.sudo().env['sna.instagram.post.hashtag'].create({'name': h})
                            hashtag_ids.append((4, hashtag.id))

                        post_data = {
                          'post_id': i['id'],
                          'date': datetime.fromtimestamp(i['taken_at']),
                          'caption': caption,
                          'like_count': i['like_count'],
                          'comment_count': i['comment_count'],
                          'hashtag_ids': hashtag_ids,
                          'location': i['location'] if 'location' in i else None,
                          'latitude': i['lat'] if 'lat' in i else None,
                          'longitude': i['lng'] if 'lng' in i else None
                        }

                        if 'location' in i:
                          print(i['location'])

                        post = self.sudo().env['sna.instagram.post'].create(post_data)

                        comments = i['preview_comments']

                        comment_ids = []

                        for c in comments:
                          comment_data = {
                            'comment_id': c['pk'],
                            'comment_text': c['text'],
                            'post_id': post.id,
                            'date': datetime.fromtimestamp(c['created_at'])
                          }

                          comment = self.sudo().env['sna.instagram.post.comment'].create(comment_data)
                          comment_ids.append(comment.id)

                        if i['media_type'] == 1 or i['media_type'] == 2:
                            images = [i['image_versions2']['candidates'][0]['url']]
                        elif i['media_type'] == 8:
                            images = [j['image_versions2']['candidates'][0]['url'] for j in i['carousel_media']]

                        for img in images:
                            img_data = {
                              'media_id': i['pk'],
                              'url': img,
                              'post_id': post.id
                            }
                            self.sudo().env['sna.instagram.post.media'].create(img_data)

                next_max_id = results.get('next_max_id')
                if next_max_id:
                    print(next_max_id)
                    results = api.self_feed(count=50, max_id=next_max_id)
                else:
                    more =False

        except Exception as e:
            print(e)
            print('\n\n')
            if e == 'bad_password':
              e = 'Senha incorreta!'
            mess= {
                    'title': ('Erro'),
                    'message' : e
                  }
            return {'warning': mess}

    @api.model
    def create(self, values):
        record = super(InstagramConfig, self).create(values)
        print('create\n\n')
        self._start_getting_posts(values)
        return record

    # def _run_inbg(self, cr, uid):
    #     self.pool.get('ir.cron').create(cr, uid, {
    #       'model': 'sna.instagram.post',
    #       'function': '_',
    #       'args': 
    #   })
