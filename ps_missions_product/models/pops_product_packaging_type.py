# Copyright 2020 - TODAY, Marcel Savegnago <marcel.savegnago@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, tools, _


class PopsProductPackagingType(models.Model):

    _name = 'pops.product.packaging.type'
    _description = 'Pops Product Packaging Type'

    name = fields.Char()
    pops_product_ids = fields.One2many(
        'pops.product',
        'packaging_type_id',
        string="Mission Products"
    )
    pops_product_count = fields.Integer(
        compute='_compute_pops_product_count',
        string='# Mission Products'
    )

    # image: all image fields are base64 encoded and PIL-supported
    image = fields.Binary(
        "Image", attachment=True,
        help="This field holds the image used as image for the product, "
             "limited to 1024x1024px.")
    image_medium = fields.Binary(
        "Medium-sized image", attachment=True,
        help="Medium-sized image of the product. It is automatically "
             "resized as a 128x128px image, with aspect ratio preserved, "
             "only when the image exceeds one of those sizes. Use this field in "
             "form views or some kanban views.")
    image_small = fields.Binary(
        "Small-sized image", attachment=True,
        help="Small-sized image of the product. It is automatically "
             "resized as a 64x64px image, with aspect ratio preserved. "
             "Use this field anywhere a small image is required.")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            tools.image_resize_images(vals)
        res = super(PopsProductPackagingType, self).create(vals_list)
        return res

    @api.multi
    def write(self, vals):
        tools.image_resize_images(vals)
        res = super(PopsProductPackagingType, self).write(vals)
        return res

    @api.depends('pops_product_ids')
    def _compute_pops_product_count(self):
        for rec in self:
            rec.pops_product_count = len(
                rec.pops_product_ids)

    @api.multi
    def action_view_pops_product(self):
        action = self.env.ref("ps_missions_product.pops_product_act_window").read()[0]
        if self.pops_product_count > 1:
            action["domain"] = [("id", "in", self.pops_product_ids.ids)]
        else:
            action["views"] = [(
                self.env.ref("ps_missions_product.pops_product_form_view").id, "form")]
            action["res_id"] = self.pops_product_ids and \
                               self.pops_product_ids.ids[0] or False
        return action