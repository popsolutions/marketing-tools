from odoo import api, models


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.multi
    def post(self):
        res = super(AccountPayment, self).post()
        measurment_list = self.mapped('invoice_ids.origin')
        measurment_ids = self.env['pops.measurement'].search([('name', 'in', measurment_list)])
        if measurment_ids:
            measurment_ids.action_mark_as_paid()
        return res
