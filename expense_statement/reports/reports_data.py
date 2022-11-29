from odoo import models, api, fields
from odoo.exceptions import UserError


class ExpenseStatementReport(models.AbstractModel):
    _name = 'report.expense_statement.expense_statement_rep_temp'
    _description = 'Expense Statement Report'

    def get_date_data(self, date, account):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        tot = sum(self.env['account.move.line'].search(
            [('account_id', '=', account.id), ('move_id.branch_id', '=', docs.branch_id.id),
             ('date', '=', date)]).mapped('debit'))
        return tot

    def get_account_total(self, account):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        tot = sum(self.env['account.move.line'].search(
            [('account_id', '=', account.id), ('move_id.branch_id', '=', docs.branch_id.id),
             ('date', '>=', docs.date_from), ('date', '<=', docs.date_to)]).mapped('debit'))
        return tot

    def get_fp_account_total(self, date):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        fb_accounts = self.env['account.account'].search([('is_fp', '=', True)])
        print(fb_accounts)
        tot = sum(self.env['account.move.line'].search(
            [('account_id', 'in', fb_accounts.ids), ('move_id.branch_id', '=', docs.branch_id.id),
             ('date', '=', date)]).mapped('debit'))
        print(tot)
        return tot

    def get_bank_account_total(self, date):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        fb_accounts = self.env['account.account'].search([('is_bank', '=', True)])
        print(fb_accounts)
        tot = sum(self.env['account.move.line'].search(
            [('account_id', 'in', fb_accounts.ids), ('move_id.branch_id', '=', docs.branch_id.id),
             ('date', '=', date)]).mapped('debit'))
        print(tot)
        return tot

    def get_sm_account_total(self, date):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        fb_accounts = self.env['account.account'].search([('is_bank', '=', True)])
        print(fb_accounts)
        tot = sum(self.env['account.move.line'].search(
            [('account_id', 'in', fb_accounts.ids), ('move_id.branch_id', '=', docs.branch_id.id),
             ('date', '=', date)]).mapped('debit'))
        print(tot)
        return tot

    @api.model
    def _get_report_values(self, docids, data=None):
        accounts = self.env['account.account'].search([('seq_no', '>', 0), ('is_fp', '=', False)], order='seq_no asc')
        # fb_accounts = self.env['account.account'].search([('seq_no', '>', 0), ('is_fp', '=', True)], order='seq_no asc')
        move_lines = self.env['account.move.line'].search([('move_id.branch_id', '=', data["form"]['branch_id'][0]), ('account_id', 'in', accounts.ids), ('date', '>=', data["form"]['date_from']), ('date', '<=', data["form"]['date_to'])], order='date asc')
        dates = move_lines.mapped('date')
        dates = list(dict.fromkeys(dates))
        return {
            'doc_ids': docids,
            'doc_model': 'menu.report1',
            'data': data['form'],
            'accounts': accounts,
            # 'fb_accounts': fb_accounts,
            'dates': dates,
            'get_date_data': self.get_date_data,
            'get_account_total': self.get_account_total,
            'get_fp_account_total': self.get_fp_account_total,
            'get_bank_account_total': self.get_bank_account_total,
            'get_sm_account_total': self.get_sm_account_total,
        }
