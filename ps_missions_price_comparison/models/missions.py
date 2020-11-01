from odoo import fields, models


class PopsMissions(models.Model):
    _inherit = 'pops.missions'

    type_mission = fields.Selection(selection_add=[('price_comparison', 'Price Comparison')])
    price_comparison_ids = fields.One2many('pops.price_comparison', 'missions_id', string='Price Comparisons')


class PopsPriceComparison(models.Model):
    _name = 'pops.price_comparison'
    _description = 'Price Comparison'

    product_id = fields.Many2one('pops.product', 'Product')
    missions_id = fields.Many2one('pops.missions', 'Mission')
