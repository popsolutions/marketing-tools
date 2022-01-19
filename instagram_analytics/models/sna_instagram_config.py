# -*- coding: utf-8 -*-

import re
from odoo import models, fields, api
from datetime import datetime
from instagram_private_api import Client, ClientCompatPatch
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
from igramscraper.instagram import Instagram

class InstagramConfig(models.Model):
    _name = 'sna.instagram.config'
    _description = 'Account'

    sna_account_name = fields.Char()
    partner_id = fields.Many2one('res.partner')
    sna_instagram_username = fields.Char()
    sna_instagram_password = fields.Char()
    context_acount_ids = fields.One2many('sna.instagram.context.acount', 'account_namelines_id', 'Account Context',
                                      readonly=True, copy=True)
    active = fields.Boolean('Active')
    login_account = fields.Boolean('Login Account')

    @api.multi
    def start_getting_posts_privateapi(self, values):
        sna_instagram_username = values['sna_instagram_username']
        sna_instagram_password = values['sna_instagram_password']

        try:
            more = True

            api = Client(sna_instagram_username, sna_instagram_password)
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
                          'config_id': values['config_id'],
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

                        query = "select id from sna_instagram_post where post_id = '" + i['id'] + "'"
                        self.env.cr.execute(query)
                        postExists = self.env.cr.fetchall()

                        if postExists:
                          post_data['id'] = postExists[0][0]
                          post = self.sudo().env['sna.instagram.post'].write(post_data)
                          post_id = post_data['id']
                        else:
                          post = self.sudo().env['sna.instagram.post'].create(post_data)
                          post_id = post.id

                          #Salvando a imagem do Post
                          if i['media_type'] == 1 or i['media_type'] == 2:
                              images = [i['image_versions2']['candidates'][0]['url']]
                          elif i['media_type'] == 8:
                              images = [j['image_versions2']['candidates'][0]['url'] for j in i['carousel_media']]

                          for img in images:
                              query = "select id from sna_instagram_post_media where url = '" + img + "' and post_id = " + str(post_id) + " limit 1"
                              self.env.cr.execute(query)
                              mediaExists = self.env.cr.fetchall()

                              if not mediaExists:
                                  img_data = {
                                    'media_id': i['pk'],
                                    'url': img,
                                    'post_id': post_id
                                  }
                                  self.sudo().env['sna.instagram.post.media'].create(img_data)

                        comments = api.media_n_comments(i['id'], n=i['comment_count'])

                        for c in comments:
                          comment_data = {
                            'comment_id': c['pk'],
                            'comment_text': c['text'],
                            'post_id': post_id,
                            'date': datetime.fromtimestamp(c['created_at'])
                          }

                          comment = self.sudo().env['sna.instagram.post.comment'].create(comment_data)

                next_max_id = results.get('next_max_id')
                if next_max_id:
                    print(next_max_id)
                    results = api.self_feed(count=50, max_id=next_max_id)
                else:
                    more =False

        except Exception as e:
          print(e)
          print('\n\n')
          if e == 'bad_password' or e == 'User credentials are wrong., Code:401':
            e = 'Senha incorreta!'
          raise UserError(e)

    @api.multi
    def start_getting_posts_instagramscrapy(self, values):
      sna_instagram_username = values['sna_instagram_username']
      config_id = values['config_id']

      try:

        instagram = Instagram()
        # instagram.with_credentials('MateusONunes', 'nunes54%$', 'path/to/cache/folder2')

        query = "select sic.sna_instagram_username, sic.sna_instagram_password from sna_instagram_config " \
                "sic where sic.active = true and sic.login_account = true" \
                " order by id limit 1"
        self.env.cr.execute(query)
        userInstagranLoginAccount = self.env.cr.fetchall()
        userLogin_userName = userInstagranLoginAccount[0][0];
        userLogin_password = userInstagranLoginAccount[0][1];
        userLogin_password = 'x';

        instagram.with_credentials(userLogin_userName, userLogin_password, 'path/to/cache/folder2')
        instagram.login()

        medias = instagram.get_medias(sna_instagram_username, 20)
        i = 0
        for media in medias:
          i += 1
          # print(media)
          account = media.owner
          # print(account)
          post_data = {
            'post_id': media.identifier,
            'config_id': config_id,
            'date': datetime.fromtimestamp(media.created_time),
            'caption': media.caption,
            'like_count': media.likes_count,
            'comment_count': str(media.comments_count),
            'hashtag_ids': '',
            'location': None,
            'latitude': None,
            'longitude': None
          }

          query = "select id from sna_instagram_post where post_id = '" + str(media.identifier) + "'"
          self.env.cr.execute(query)
          postExists = self.env.cr.fetchall()

          if not postExists:
            post = self.sudo().env['sna.instagram.post'].create(post_data)
            post_id = post.id

            images = [media.square_images[0]]

            for img in images:
              img_data = {
                'media_id': media.identifier,
                'url': img,
                'post_id': post_id
              }
              self.sudo().env['sna.instagram.post.media'].create(img_data)

          else:
            post_data['id'] = postExists[0][0]
            # post = self.sudo().env['sna.instagram.post'].write(post_data)
            post_id = post_data['id']

          comments = instagram.get_media_comments_by_id(media.identifier, 50)

          for comment in comments['comments']:
            # print(comment.owner.username + ': ' + comment.text)
            query = "select id from sna_instagram_post_comment where comment_text = '" + comment.text + "' and post_id = " + str(post_id) + " limit 1"
            self.env.cr.execute(query)
            commentExists = self.env.cr.fetchall()

            if not commentExists:
                comment_data = {
                  'comment_id': comment.identifier,
                  'comment_text': comment.text,
                  'post_id': post_id,
                  'date': datetime.fromtimestamp(float(comment.created_at))
                }

                comment = self.sudo().env['sna.instagram.post.comment'].create(comment_data)

      except Exception as e:
          print(e)
          print('\n\n')
          if e.args[0] == 'bad_password' or e.args[0] == 'User credentials are wrong., Code:401':
            e = 'Senha incorreta!'
          raise UserError(e)

    @api.multi
    def action_getposts(self, values):
      self._start_getting_posts({'sna_instagram_username':self.sna_instagram_username,
                                 'sna_instagram_password': self.sna_instagram_password,
                                 'id':self.id})

    @api.model
    def _start_getting_posts(self, values):
        if (not values['sna_instagram_password']):
          self.start_getting_posts_instagramscrapy({'sna_instagram_username': values['sna_instagram_username'],
                                                    'config_id': values['id']})
        else:
          self.start_getting_posts_privateapi({'sna_instagram_username': values['sna_instagram_username'],
                                               'sna_instagram_password': values['sna_instagram_password'],
                                               'config_id': values['id']})

    @api.model
    def _start_getting_posts_all(self):
      configs = self.env['sna.instagram.config'].search([('active', '=', True)])
      for config in configs:
        self._start_getting_posts(config)

    @api.model
    def create(self, values):
        record = super(InstagramConfig, self).create(values)
        print('create\n\n')

        if values['active']:
          self._start_getting_posts(record)
        return record

    # def _run_inbg(self, cr, uid):
    #     self.pool.get('ir.cron').create(cr, uid, {
    #       'model': 'sna.instagram.post',
    #       'function': '_',
    #       'args': 
    #   })


class SnaInstagramConfigContextAcount(models.Model):
  _name = 'sna.instagram.context.acount'
  _description = 'Context'

  context_description = fields.Char('Context Description')
  account_namelines_id = fields.Many2one('sna.instagram.config', 'Account name', ondelete='cascade', required=True)
  def name_get (self):
    result = []

    for record in self:
      result.append((record.id, record.context_description))
    return result
