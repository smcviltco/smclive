# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import ValidationError, UserError


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    def unlink(self):
        for rec in self:
            rec.remove_attachment()
            # if not rec.env.user.has_group('stock.group_stock_manager') and rec.res_model in ['stock.picking']:
            #     raise ValidationError("Sorry, you are not allowed to delete the attachment.")
        return super(IrAttachment, self).unlink()

    def remove_attachment(self):
        data = "<strong>File: '%s' is Deleted By User: %s </strong>" % (self.name, self.env.user.name)
        message = _("%s") % (data)
        doc = self.env['stock.picking'].browse([self.res_id])
        return doc.message_post(body=message)

    def add_attachment(self):
        data = "<strong>File: '%s' is Uploaded By User: %s </strong>" % (self.name, self.env.user.name)
        message = _("%s") % (data)
        doc = self.env['stock.picking'].browse([self.res_id])
        return doc.message_post(body=message)

    @api.model
    def create(self, vals_list):
        rec = super().create(vals_list)
        rec.add_attachment()
        return rec



