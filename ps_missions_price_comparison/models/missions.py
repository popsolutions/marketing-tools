from odoo import fields, models
from odoo.addons.ps_missions.models.missions import MISSION_PRODUCT

MISSION_PRODUCT.update(
    {'price_comparison': 'ps_missions_price_comparison.product_mission_price_comparison'}
)


class PopsMissions(models.Model):
    _inherit = 'pops.missions'

    type_mission = fields.Selection(selection_add=[('price_comparison', 'Price Comparison')])
    price_comparison_ids = fields.One2many('pops.price_comparison', 'missions_id', string='Price Comparisons')


class PopsPriceComparison(models.Model):
    _name = 'pops.price_comparison'
    _description = 'Price Comparison'

    product_id = fields.Many2one('pops.product', 'Product')
    missions_id = fields.Many2one('pops.missions', 'Mission')
