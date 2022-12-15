# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartnerInh(models.Model):
    _inherit = 'res.partner'

    secondary_name = fields.Char()