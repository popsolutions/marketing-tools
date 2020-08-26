from odoo import api, fields, models


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    @api.multi
    def _compute_missions_count(self):
        missions = self.env['pops.missions']
        for partner in self:
            partner.missions_count = missions.search_count([('partner_id', '=', partner.id)])

    missions_count = fields.Integer(compute='_compute_missions_count', string='Missions Count', type='integer',
                                    groups='ps_missions.group_missions_user')
    is_oper = fields.Boolean('Is a Mission Oper', help="Check if is a Mission Operator")