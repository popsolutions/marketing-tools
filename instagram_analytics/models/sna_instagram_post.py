# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InstagramPost(models.Model):
    _name = 'sna.instagram.post'
    _description = 'Instagram Post'

    post_id = fields.Char("Instagram Post ID")
    config_id = fields.Many2one('sna.instagram.config')
    partner_id = fields.Many2one('res.partner', related='config_id.partner_id', readonly=True, store=True)
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
            if len(self.media_ids) > 0:
                img_url = self.media_ids[0].url
                elem.img_attach = '<img src="%s"/>' % img_url

class InstagramPostMedia(models.Model):
    _name = 'sna.instagram.post.media'

    media_id = fields.Char()
    url = fields.Char()
    post_id = fields.Many2one('sna.instagram.post', ondelete='cascade')


class InstagramPostHashtag(models.Model):
    _name = 'sna.instagram.post.hashtag'

    name = fields.Char()
    post_id = fields.Many2one('sna.instagram.post', ondelete='cascade')


class InstagramPostComment(models.Model):
    _name = 'sna.instagram.post.comment'
    _description = 'Post Comments'

    comment_id = fields.Char("Comment Id")
    comment_text = fields.Text()
    post_id = fields.Many2one('sna.instagram.post', ondelete='cascade', string='Post id')
    post_id_ = fields.Integer(string='Id Post', related='post_id.id', readonly=True, store=True)
    post_post_id = fields.Char(string='Post id Instagram', related='post_id.post_id', readonly=True, store=True)
    partner_id = fields.Many2one('res.partner', related='post_id.partner_id', readonly=True, store=True)
    config_id = fields.Many2one('sna.instagram.config', related='post_id.config_id', readonly=True, store=True)
    context_id = fields.Many2one('sna.instagram.context.acount', string = 'Context')
    context_description = fields.Char(related='context_id.context_description', readonly=True)
    context_sentiment = fields.Selection([('1', 'Positivo'), ('2', 'Negativo'), ('3', 'Neutro')], string='Context Sentiment')
    date = fields.Datetime()
