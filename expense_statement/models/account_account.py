from odoo import models, fields, api
from odoo.exceptions import UserError


class AccountMoveInherited(models.Model):
    _inherit = 'account.move'

    is_inter_branch_transfer = fields.Boolean()

    def action_add_branch(self):
        moves = self.env['account.move.line'].search([('branch_id', '=', False)])
        for rec in moves:
                rec.branch_id = rec.move_id.branch_id.id


class AccountPaymentInherited(models.Model):
    _inherit = 'account.payment'

    is_sale_return = fields.Boolean()
    # available_partner_bank_ids = fields.Many2many('res.bank')


class AccountAccountInherited(models.Model):
    _inherit = 'account.account'

    seq_no = fields.Integer('Sequence No')
    secondary_name = fields.Char()
    is_fp = fields.Boolean()
    is_bank = fields.Boolean()
    is_sm = fields.Boolean()
    # is_head_office = fields.Boolean()
    is_other_expense = fields.Boolean()
    statements_branch = fields.Many2one('res.branch')

    @api.constrains('seq_no')
    def check_code(self):
        if self.seq_no:
            code = self.env['account.account'].search([('seq_no', '=', self.seq_no)])
            if len(code) > 1:
                raise UserError('Sequence Already Exist')
