# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InstagramPost(models.Model):
    _name = 'sna.instagram.post'

    post_id = fields.Char("Instagram Post ID")
    date = fields.Datetime()
    caption = fields.Text()
    like_count = fields.Integer()
    comment_count = fields.Integer()
    location = fields.Char()
    latitude = fields.Char()
    longitude = fields.Char()
    
    media_ids = fields.One2many('sna.instagram.post.media', 'post_id')
    hashtag_ids = fields.One2many('sna.instagram.post.hashtag', 'post_id')
    comment_ids = fields.One2many('sna.instagram.post.comment', 'post_id')

    img_attach = fields.Html('Image', compute="_get_img_html")

    def _get_img_html(self):
        for elem in self:
            img_url = self.media_ids[0].url
            elem.img_attach = '<img src="%s"/>' % img_url

class InstagramPostMedia(models.Model):
    _name = 'sna.instagram.post.media'

    media_id = fields.Char()
    url = fields.Char()
    post_id = fields.Many2one('sna.instagram.post')


class InstagramPostHashtag(models.Model):
    _name = 'sna.instagram.post.hashtag'

    name = fields.Char()
    post_id = fields.Many2one('sna.instagram.post')


class InstagramPostComment(models.Model):
    _name = 'sna.instagram.post.comment'

    comment_id = fields.Char()
    comment_text = fields.Text()
    post_id = fields.Many2one('sna.instagram.post')
    date = fields.Datetime()
