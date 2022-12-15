# -*- coding: utf-8 -*-
# from odoo import http


# class PartnerSecondName(http.Controller):
#     @http.route('/partner_second_name/partner_second_name/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/partner_second_name/partner_second_name/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('partner_second_name.listing', {
#             'root': '/partner_second_name/partner_second_name',
#             'objects': http.request.env['partner_second_name.partner_second_name'].search([]),
#         })

#     @http.route('/partner_second_name/partner_second_name/objects/<model("partner_second_name.partner_second_name"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('partner_second_name.object', {
#             'object': obj
#         })
