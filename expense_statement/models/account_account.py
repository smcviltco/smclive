from odoo import models, fields


class AccountMoveInherited(models.Model):
    _inherit = 'account.move'

    def action_add_branch(self):
        moves = self.env['account.move.line'].search([('branch_id', '=', False)])
        for rec in moves:
                rec.branch_id = rec.move_id.branch_id.id


class AccountAccountInherited(models.Model):
    _inherit = 'account.account'

    seq_no = fields.Integer('Sequence No')
