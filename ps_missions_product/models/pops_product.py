# Copyright 2020 - TODAY, Marcel Savegnago <marcel.savegnago@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, tools, _


class PopsProduct(models.Model):

    _name = 'pops.product'
    _description = 'Pops Product'  # TODO

    name = fields.Char()

    default_code = fields.Char('Internal Reference', index=True)

    category_id = fields.Many2one(
        'pops.product.category', 'Product Category',
        help="Select category for the current product")

    brand_id = fields.Many2one(
        'pops.product.brand', 'Product Brand',
        help="Select brand for the current product")

    barcode = fields.Char(
        'Barcode', copy=False, oldname='ean13',
        help="International Article Number used for product identification.")

    # image: all image fields are base64 encoded and PIL-supported
    image = fields.Binary(
        "Image", attachment=True,
        help="This field holds the image used as image for the product, limited to 1024x1024px.")
    image_medium = fields.Binary(
        "Medium-sized image", attachment=True,
        help="Medium-sized image of the product. It is automatically "
             "resized as a 128x128px image, with aspect ratio preserved, "
             "only when the image exceeds one of those sizes. Use this field in form views or some kanban views.")
    image_small = fields.Binary(
        "Small-sized image", attachment=True,
        help="Small-sized image of the product. It is automatically "
             "resized as a 64x64px image, with aspect ratio preserved. "
             "Use this field anywhere a small image is required.")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            tools.image_resize_images(vals)
        res = super(PopsProduct, self).create(vals_list)
        return res

    @api.multi
    def write(self, vals):
        tools.image_resize_images(vals)
        res = super(PopsProduct, self).write(vals)
        return res