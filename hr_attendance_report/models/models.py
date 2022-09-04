from odoo import models, fields, api


class UserdataInh(models.Model):
    _inherit = 'user.attendance'

    address_id = fields.Many2one('res.partner')
    department_id = fields.Many2one('hr.department')

#     bonus = fields.Float('Bonus', compute="_compute_bonus")
#
#     def _compute_bonus(self):
#         for record in self:
#             rec = self.env['hr.contract'].search([('employee_id', '=', record.employee_id.id)])
#             for r in rec:
#                 record.bonus = r.bonus
