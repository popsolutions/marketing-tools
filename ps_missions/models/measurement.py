# -*- coding: utf-8 -*-

import json

from odoo import api, fields, models, tools, SUPERUSER_ID, _


MEASUREMENT_PRODUCT = {
    'quizz': 'ps_missions.product_measurement_quizz',
    'photo': 'ps_missions.product_measurement_photo',
    'double': 'ps_missions.product_measurement_quizz_and_photo'
}


class PopsMeasurement(models.Model):
    _name = 'pops.measurement'
    _description = 'Measurement'
    _order = 'priority desc, sequence, id desc'

    name = fields.Char('Name', default=lambda self: _('New'), copy=False)
    partner_id = fields.Many2one('res.partner', 'Vendor')
    state = fields.Selection([('draft', 'Draft'),
                              ('ordered', 'Ordered'),
                              ('doing', 'Doing'),
                              ('done', 'Done'),
                              ('approved', 'Approved'),
                              ('paid', 'Paid')],
                             default='draft', string='State', copy=False)
    date_started = fields.Date('Date Started')
    date_finished = fields.Date('Date Finished')
    measurement_latitude = fields.Float('Geo Latitude', digits=(16, 5))
    measurement_longitude = fields.Float('Geo Longitude', digits=(16, 5))
    google_map_measurement = fields.Char(string='Map')
    lines_ids = fields.One2many('pops.measurement.lines', 'measurement_id', 'Measurement Lines', readonly=True,
                                copy=True)
    quizz_lines_ids = fields.One2many('pops.measurement.quizzlines', 'measurement_id', 'Measurement Quizz Lines',
                                      readonly=True, copy=True)
    photo_lines_ids = fields.One2many('pops.measurement.photolines', 'measurement_id', 'Measurement Photo Lines',
                                      readonly=True, copy=True)
    price_comparison_lines_ids = fields.One2many('pops.measurement.price_comparison.lines', 'measurement_id',
                                                 'Measurement Photo Lines', readonly=False, copy=True)
    missions_id = fields.Many2one('pops.missions', 'Missions', ondelete='cascade', required=True)
    color = fields.Integer(string='Color Index')
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
    ], default='0', index=True, string='Priority')
    sequence = fields.Integer(string='Sequence', index=True, default=10,
                              help='Gives the sequence order when displaying a list of measurement.')
    active = fields.Boolean(default=True)
    kanban_state = fields.Selection([
        ('draft', 'Grey'),
        ('ordered', 'Yellow'),
        ('doing', 'Green'),
        ('done', 'Blue')], string='Kanban State',
        copy=False, default='draft', required=True)
    kanban_state_label = fields.Char(compute='_compute_kanban_state_label', string='Kanban State Label',
                                     track_visibility='onchange')
    legend_priority = fields.Char(
        string='Starred Explanation', translate=True,
        help='Explanation text to help users using the star on tasks or issues in this stage.')
    legend_blocked = fields.Char(
        'Yellow Kanban Label', default=lambda s: _('Ready'), translate=True, required=True,
        help='Override the default value displayed for the blocked state for kanban selection, when the task or issue '
             'is in that stage.')
    legend_done = fields.Char(
        'Blue Kanban Label', default=lambda s: _('Done'), translate=True, required=True,
        help='Override the default value displayed for the done state for kanban selection, when the task or issue is '
             'in that stage.')
    legend_normal = fields.Char(
        'Grey Kanban Label', default=lambda s: _('Pending'), translate=True, required=True,
        help='Override the default value displayed for the normal state for kanban selection, when the task or issue '
             'is in that stage.')
    legend_doing = fields.Char(
        'Green Kanban Label', default=lambda s: _('In Progress'), translate=True, required=True,
        help='Override the default value displayed for the normal state for kanban selection, when the task or issue '
             'is in that stage.')

    @api.onchange('measurement_latitude', 'measurement_longitude')
    def compute_get_google_map(self):
        # maps_loc = {u'position': {u'lat': self.measurement_latitude, u'lng': self.measurement_longitude}, u'zoom': 3}
        # maps_loc = {u'position': {u'lat': 20.593684, u'lng': 78.96288}, u'zoom': 3}
        maps_loc = {
            'position': {'lat': self.measurement_latitude, 'lng': self.measurement_longitude},
            'zoom': 3
        }
        json_map = json.dumps(maps_loc)
        self.google_map_measurement = json_map

    @api.depends('state', 'kanban_state')
    def _compute_kanban_state_label(self):
        for task in self:
            if task.kanban_state == 'draft':
                task.kanban_state_label = task.legend_normal
            elif task.kanban_state == 'ordered':
                task.kanban_state_label = task.legend_blocked
            elif task.kanban_state == 'doing':
                task.kanban_state_label = task.legend_blocked
            else:
                task.kanban_state_label = task.legend_done

    @api.multi
    def action_confirm(self):
        for rec in self:
            rec.set_name_sequence()
            rec.state = 'ordered'

    @api.multi
    def action_doing(self):
        self.state = 'doing'

    @api.multi
    def action_done(self):
        self.state = 'done'

    @api.multi
    def _create_vendor_invoice(self):
        product_id = self.env.ref(MEASUREMENT_PRODUCT.get(
            self.missions_id.type_mission, None))
        account_id = product_id.product_tmpl_id.get_product_accounts()['expense']
        inv_line_vals = {
            'product_id': product_id.id,
            'name': product_id.description,
            'price_unit': self.missions_id.reward,
            'account_id': account_id.id,
            'invoice_line_tax_ids': [(6, 0, product_id.supplier_taxes_id.ids)],
        }
        inv_data = {
            'type': 'in_invoice',
            'reference': self.name,
            'account_id': self.partner_id.property_account_payable_id.id,
            'partner_id': self.partner_id.id,
            'origin': self.name,
            'invoice_line_ids': [(0, 0, inv_line_vals)],
        }
        self.sudo().env['account.invoice'].create(inv_data)

    @api.multi
    def action_approve(self):
        self._create_vendor_invoice()
        self.state = 'approved'

    @api.multi
    def action_mark_as_paid(self):
        for rec in self:
            rec.state = 'paid'

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.model
    def set_name_sequence(self):
        if self.name == _('New') and self.state == 'draft':
            self.name = self.env['ir.sequence'].next_by_code('mission.measurement') or _('New')


class PopsMeasurementLine(models.Model):
    _name = 'pops.measurement.lines'
    _description = 'Measurement Lines'

    name = fields.Char('Quizz/Descriptions')
    type = fields.Selection([('quizz', 'Quizz'), ('photo', 'Photo'), ('double', 'Quizz and Photo')], default='quizz',
                            string='Type')
    answer = fields.Text('Answer')
    photo = fields.Binary('Photo')
    photo_name = fields.Char('Photo Name')
    measurement_id = fields.Many2one('pops.measurement', 'Measurement', ondelete='cascade', required=True)


class PopsMeasurementQuizzLine(models.Model):
    _name = 'pops.measurement.quizzlines'
    _description = 'Measurement Quizz Lines'

    name = fields.Char('Quizz Answers')
    quizz_id = fields.Many2one('pops.quizz', 'Quizz', ondelete='cascade', required=True)
    alternative_id = fields.Many2one('pops.alternative', 'Alternative', ondelete='cascade', required=True)
    measurement_id = fields.Many2one('pops.measurement', 'Measurement', ondelete='cascade', required=True)


class PopsMeasurementPhotoLine(models.Model):
    _name = 'pops.measurement.photolines'
    _description = 'Measurement Photo Lines'

    name = fields.Char('Photo Name')
    photo = fields.Binary('Photo')
    photo_id = fields.Many2one('pops.photo.lines', 'Photo Line', ondelete='cascade', required=True)
    measurement_id = fields.Many2one('pops.measurement', 'Measurement', ondelete='cascade', required=True)


class PopsMeasurementPriceComparison(models.Model):
    _name = 'pops.measurement.price_comparison.lines'
    _description = 'Measurement Price Comparison'

    measurement_id = fields.Many2one('pops.measurement', 'Measurement', ondelete='cascade', required=True)
    comparison_id = fields.Many2one('pops.price_comparison', 'Price Comparison')
    # product_id = fields.Many2one('missions.product', 'Product') #ToDo: merge with products PR
    product_id = fields.Char('Product')
    price = fields.Float('Price')
    photo = fields.Binary('Photo', help='Photo of the shelf')
    # competitor_ids = fields.Many2many('res.partner', 'Competitors')
    competitor_ids = fields.Char('Competitors') #ToDo: merge with products PR
