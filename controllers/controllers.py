# -*- coding: utf-8 -*-
from odoo import http

# class DsaModulo(http.Controller):
#     @http.route('/dsa_modulo/dsa_modulo/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dsa_modulo/dsa_modulo/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dsa_modulo.listing', {
#             'root': '/dsa_modulo/dsa_modulo',
#             'objects': http.request.env['dsa_modulo.dsa_modulo'].search([]),
#         })

#     @http.route('/dsa_modulo/dsa_modulo/objects/<model("dsa_modulo.dsa_modulo"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dsa_modulo.object', {
#             'object': obj
#         })