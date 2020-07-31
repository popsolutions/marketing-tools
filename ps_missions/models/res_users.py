from odoo import api, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def create(self, vals):
        return super(ResUsers, self.with_context(no_reset_password=True)).create(vals)
