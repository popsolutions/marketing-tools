from odoo import fields, models
from odoo.addons.ps_missions.models.measurement import MEASUREMENT_PRODUCT

MEASUREMENT_PRODUCT.update(
    {'price_comparison': 'ps_missions_price_comparison.product_mission_price_comparison'}
)


class PopsMeasurement(models.Model):
    _inherit = 'pops.measurement'

    price_comparison_lines_ids = fields.One2many('pops.measurement.price_comparison.lines', 'measurement_id',
                                                 'Measurement Photo Lines', readonly=False, copy=True)


class PopsMeasurementPriceComparison(models.Model):
    _name = 'pops.measurement.price_comparison.lines'
    _description = 'Measurement Price Comparison'

    measurement_id = fields.Many2one('pops.measurement', 'Measurement', ondelete='cascade', required=True)
    comparison_id = fields.Many2one('pops.price_comparison', 'Price Comparison')
    product_id = fields.Many2one('pops.product', 'Product')
    price = fields.Float('Price')
    photo = fields.Binary('Photo', help='Photo of the shelf')
    competitor_ids = fields.Many2many('pops.product', string='Competitors')
