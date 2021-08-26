# -*- coding: utf-8 -*-
# from odoo import http


# class Ahmed(http.Controller):
#     @http.route('/ahmed/ahmed/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ahmed/ahmed/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ahmed.listing', {
#             'root': '/ahmed/ahmed',
#             'objects': http.request.env['ahmed.ahmed'].search([]),
#         })

#     @http.route('/ahmed/ahmed/objects/<model("ahmed.ahmed"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ahmed.object', {
#             'object': obj
#         })
