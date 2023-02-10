# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import ValidationError

MISSION_PRODUCT = {
    'quizz': 'ps_missions.product_mission_quizz',
    'photo': 'ps_missions.product_mission_photo',
    'double': 'ps_missions.product_mission_quizz_and_photo',
}


class PopsMissions(models.Model):
    _name = 'pops.missions'
    _description = 'Missions'

    @api.multi
    def _compute_measurement_count(self):
        measurement = self.env['pops.measurement']
        for missions in self:
            missions.measurement_count = measurement.search_count([('missions_id', '=', missions.id)])

    # @api.multi
    # def _compute_rewarded_count(self):
    #     measurement = self.env['pops.measurement']
    #     for missions in self:
    #         rewards = 0.0
    #         measurement.search([('approved', '=', True)], limit=1).
    #         missions.rewarded_count = measurement.search_count([
    #             ('missions_id', '=', missions.id), 
    #             ('approved', '=', True)])

    # @api.multi
    # def _compute_paid_count(self):
    #     measurement = self.env['pops.measurement']
    #     for missions in self:
    #         missions.paid_count = measurement.search_count([
    #             ('missions_id', '=', missions.id), 
    #             ('approved', '=', True),
    #             ('paid', '=', True)])

    name = fields.Char('Mission Title', required=True)
    state = fields.Selection([('draft', 'Draft'), ('open', 'Open'), ('closed', 'Closed')],
                             default='draft', string='State')
    create_by_user_id = fields.Many2one('res.users', 'User', default=lambda self: self.env.uid)
    partner_id = fields.Many2one('res.partner', 'Partner', required=True)
    subject = fields.Char('Subject')
    instructions = fields.Text('Instructions')
    type_mission = fields.Selection([('quizz', 'Quizz'),
                                     ('photo', 'Photo'),
                                     ('double', 'Quizz and Photo'),
                                     ],
                                    default='quizz', string='Type', required=True)
    date_create = fields.Date('Date Start')
    date_finished = fields.Date('Date Finished')
    closed = fields.Boolean('Closed?')    
    email = fields.Char('e-mail')
    priority = fields.Integer('Priority')
    account_anality = fields.Char('Account Anality')   
    contract = fields.Char('Contract')
    mission_map = fields.Char(string='Map')
    limit = fields.Integer('Limit') 
    scores = fields.Float(string='Scores')
    reward = fields.Float(string='Reward', required=True)
    photo_ids = fields.One2many('pops.photo.lines', 'mission_id', 'Photo Lines', readonly=True, copy=True)
    quizz_ids = fields.One2many('pops.quizz', 'missions_id', 'Quizz Lines', readonly=True, copy=True)
    measurement_count = fields.Integer(compute='_compute_measurement_count', string='Measurement Count', type='integer',
                                       groups='ps_missions.group_missions_user')
    establishment_id = fields.Many2one('pops.establishment', 'Establishment', ondelete='cascade', required=True)
    # reward_count = fields.Float(compute='_compute_reward_count', string='Reward', type='float',
    #                             groups='ps_missions.group_missions_user')
    
    # def _calculate_distance(self):
    #     origin = (30.172705, 31.526725)  # (latitude, longitude) don't confuse
    #     dist = (30.288281, 31.732326)

    #     # print(geodesic(origin, dist).meters)  # 23576.805481751613
    #     # print(geodesic(origin, dist).miles)  # 14.64994773134371
    #     return geodesic(origin, dist).kilometers)  # 23.576805481751613

    @api.multi
    def _check_existing_invoice(self):
        """Check if invoice already exists, in case Re-Open missions"""
        return self.env['account.invoice'].search([('origin', '=', self.name)])

    @api.multi
    def _create_customer_invoice(self):
        product_id = self.env.ref(MISSION_PRODUCT.get(
            self.type_mission, None))
        account_id = product_id.product_tmpl_id.get_product_accounts()['income']
        inv_line_vals = {
            'product_id': product_id.id,
            'name': product_id.description,
            'price_unit': self.reward,
            'account_id': account_id.id,
            'invoice_line_tax_ids': [(6, 0, product_id.taxes_id.ids)],
        }
        inv_data = {
            'type': 'out_invoice',
            'account_id': self.partner_id.property_account_receivable_id.id,
            'partner_id': self.partner_id.id,
            'origin': self.name,
            'invoice_line_ids': [(0, 0, inv_line_vals)],
        }
        self.sudo().env['account.invoice'].create(inv_data)

    @api.multi
    def action_open(self):
        """Open the mission (confirm)"""
        if not self._check_existing_invoice():
            self._create_customer_invoice()
        self.state = 'open'

    @api.multi
    def action_close(self):
        """Close the mission"""
        self.state = 'closed'

    @api.multi
    def action_draft(self):
        """Get Back mission to Draft"""
        self.state = 'draft'

    @api.multi
    def action_open_missions_measurement(self):
        return {
            'name': _('measurement'),
            'domain': [('missions_id', '=', self.id)],
            'view_type': 'form',
            'res_model': 'pops.measurement',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window'
        }

class PopsPhotoLine(models.Model):
    _name = 'pops.photo.lines'
    _description = 'Photo Lines' 
    
    name = fields.Char(string='Description')
    mission_id = fields.Many2one('pops.missions', 'Mission', ondelete='cascade', required=True)


class PopsAlternative(models.Model):
    _name = 'pops.alternative'
    _description = 'Alternative'

    name = fields.Char('Text')


class PopsQuizz(models.Model):
    _name = 'pops.quizz'
    _description = 'Quizz'

    name = fields.Char('Question')
    quizz_line_ids = fields.One2many('pops.quizz.lines', 'quizz_id', 'Quizz Lines', readonly=True, copy=True)
    missions_id = fields.Many2one('pops.missions', 'Missions', ondelete='cascade', required=True)


class PopsQuizzLine(models.Model):
    _name = 'pops.quizz.lines'
    _description = 'Quizz Lines' 
        
    alternative_id = fields.Many2one('pops.alternative', 'Alternative', ondelete='cascade', required=True)
    correct = fields.Boolean('Is Correct?')
    quizz_id = fields.Many2one('pops.quizz', 'Quizz', ondelete='cascade', required=True)


class PopsEstablishment(models.Model):
    _name = 'pops.establishment'
    _description = 'Establishment'

    name = fields.Char('Name', required=True)
    type_id = fields.Many2one('pops.establishment.type', 'Type', required=True)
    zip_code = fields.Char('Zip Code')
    address = fields.Char('Address')
    neighbor = fields.Char('Neighbor')
    city = fields.Char('City')
    state = fields.Char('State')
    latitude = fields.Char('Latitude')
    longitude = fields.Char('Longitude')

    @api.constrains('latitude')
    def _check_latitude(self):
        for lat in self:
            if ',' in lat.latitude:
                raise ValidationError("Use dot (.) instead of comma for decimals")

            try:
                float(lat.latitude)
            except Exception as e:
                raise ValidationError("Insert a valid number for latitude\n" + str(e))
                
            if not -90 <= float(lat.latitude) <= 90:
                raise ValidationError("Insert a valid number for latitude (between -90 and 90)")

    @api.constrains('longitude')
    def _check_longitude(self):
        for lon in self:
            if ',' in lon.longitude:
                raise ValidationError("Use dot (.) instead of comma for decimals")

            try:
                float(lon.longitude)
            except Exception as e:
                raise ValidationError("Insert a valid number for latitude\n" + str(e))
                
            if not -180 <= float(lon.longitude) <= 180:
                raise ValidationError("Insert a valid number for latitude (between -180 and 180)")

class PopsEstablishmentType(models.Model):
    _name = 'pops.establishment.type'
    _description = 'Establishment Type'

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
