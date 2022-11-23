from odoo import models, fields, api
from odoo.exceptions import UserError


class AccountMoveInherited(models.Model):
    _inherit = 'account.move'

    def action_add_branch(self):
        moves = self.env['account.move.line'].search([('branch_id', '=', False)])
        for rec in moves:
                rec.branch_id = rec.move_id.branch_id.id


class AccountAccountInherited(models.Model):
    _inherit = 'account.account'

    seq_no = fields.Integer('Sequence No')
    secondary_name = fields.Char()

    @api.constrains('seq_no')
    def check_code(self):
        if self.seq_no:
            code = self.env['account.account'].search([('seq_no', '=', self.seq_no)])
            if len(code) > 1:
                raise UserError('Sequence Already Exist')
