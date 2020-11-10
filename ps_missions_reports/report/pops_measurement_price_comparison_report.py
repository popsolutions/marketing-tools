# Copyright 2020 - TODAY, Marcel Savegnago <marcel.savegnago@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import os
from os.path import join as opj

from odoo import api, fields, models, tools


class PopsMeasurementPriceComparasionReport(models.Model):

    _name = 'pops.measurement.price_comparison.report'
    _description = 'Measurement Price Comparasion Report'
    _auto = False
    _rec_name = 'id'

    missions_id = fields.Many2one('pops.missions',
                                 'Mission',
                                 readonly=True)

    product_id = fields.Many2one('pops.product',
                                 'Product',
                                 readonly=True)

    brand_id = fields.Many2one('pops.product.brand',
                               'Brand',
                               readonly=True)

    category_id = fields.Many2one('pops.product.category',
                                  'Category',
                                  readonly=True)

    packaging_type_id = fields.Many2one('pops.product.packaging.type',
                                        'Packaging Type',
                                        readonly=True)

    price = fields.Float('Price')

    measurement_latitude = fields.Float('Geo Latitude',
                                        digits=(16, 5))

    measurement_longitude = fields.Float('Geo Longitude',
                                         digits=(16, 5))

    def _select(self):
        return """
            SELECT
                CAST(row_number() OVER (ORDER BY t1.id) as integer) AS id,
                t3.missions_id,
                t1.product_id,
                t2.brand_id,
                t2.category_id,
                t2.packaging_type_id,
                t1.price,
                t3.measurement_latitude,
                t3.measurement_longitude
        """

    def _from(self):
        return """
            FROM pops_measurement_price_comparison_lines AS t1
        """

    def _join(self):
        return """
            JOIN pops_product AS t2 ON t1.product_id = t2.id
            JOIN pops_measurement AS t3 ON t1.measurement_id = t3.id
        """

    def _where(self):
        return """
            WHERE
                t1.product_id IS NOT NULL
        """

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                %s
                %s
                %s
                %s
            )
        """ % (self._table, self._select(), self._from(), self._join(), self._where())
        )
