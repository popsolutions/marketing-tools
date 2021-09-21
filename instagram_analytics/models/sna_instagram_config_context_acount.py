# -*- coding: utf-8 -*-

import re
from odoo import models, fields, api
from datetime import datetime
from instagram_private_api import Client, ClientCompatPatch
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

class SnaInstagramContextAcount(models.Model):
    _name = 'sna_instagram_context_acount'

    # instconfig_id = fields.Many2one('sna.instagram.config')
    context_description = fields.Char()
    context_sentiment =  fields.Selection([('Positivo','1'),('Negativo','2'),('Neutro','3')])
    account_namelines_ids = fields.One2many('sna_instagram_context_acount.account_namelines', 'account_name_id', 'Account Name', readonly=True, copy=True)

