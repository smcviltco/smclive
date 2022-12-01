from odoo import models, api, fields
from odoo.exceptions import UserError
import datetime

class ExpenseStatementReport(models.AbstractModel):
    _name = 'report.expense_statement.expense_statement_rep_temp'
    _description = 'Expense Statement Report'

    def get_date_data(self, date, account):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        tot = sum(self.env['account.move.line'].search(
            [('account_id', '=', account.id),('move_id.state', '=', 'posted'), ('move_id.branch_id', '=', docs.branch_id.id),
             ('date', '=', date)]).mapped('debit'))
        return tot

    def get_account_total(self, account):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        tot = sum(self.env['account.move.line'].search(
            [('account_id', '=', account.id), ('move_id.branch_id', '=', docs.branch_id.id),
             ('date', '>=', docs.date_from),('move_id.state', '=', 'posted'), ('date', '<=', docs.date_to)]).mapped('debit'))
        return tot

    def get_fp_account_total(self, date):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        fb_accounts = self.env['account.account'].search([('is_fp', '=', True)])
        tot = sum(self.env['account.move.line'].search(
            [('account_id', 'in', fb_accounts.ids),('move_id.state', '=', 'posted'), ('branch_id', '=', docs.branch_id.id),
             ('date', '=', date)]).mapped('debit'))
        return tot

    def get_bank_account_total(self, date):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        fb_accounts = self.env['account.account'].search([('is_bank', '=', True)])
        tot = sum(self.env['account.move.line'].search(
            [('account_id', 'in', fb_accounts.ids),('move_id.state', '=', 'posted'), ('branch_id', '=', docs.branch_id.id),
             ('date', '=', date)]).mapped('debit'))
        return tot

    def get_sm_account_total(self, date):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        fb_accounts = self.env['account.account'].search([('is_bank', '=', True)])
        tot = sum(self.env['account.move.line'].search(
            [('account_id', 'in', fb_accounts.ids), ('move_id.state', '=', 'posted'),('branch_id', '=', docs.branch_id.id),
             ('date', '=', date)]).mapped('debit'))
        return tot

    def get_total_sale(self, date):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        fb_accounts = self.env['account.account'].search(['|', ('is_bank', '=', True), ('is_sm', '=', True)])
        tot = sum(self.env['account.move.line'].search(
            [('account_id', 'in', fb_accounts.ids),('move_id.state', '=', 'posted'), ('branch_id', '=', docs.branch_id.id),('move_id.is_inter_branch_transfer', '=', False),
             ('date', '=', date)]).mapped('debit'))
        return tot

    def get_total_sale_return(self, date):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        fb_accounts = self.env['account.account'].search(['|', ('is_bank', '=', True), ('is_sm', '=', True)])
        tot = sum(self.env['account.move.line'].search(
            [('account_id', 'in', fb_accounts.ids), ('move_id.state', '=', 'posted'),('branch_id', '=', docs.branch_id.id),('payment_id.is_sale_return', '=', True),
             ('date', '=', date)]).mapped('credit'))
        return tot

    def get_total_purchases(self, date):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        partners = self.env['res.partner'].search([('partner_type', '=', 'local_vendor')])
        fb_accounts = self.env['account.account'].search(['|', ('is_bank', '=', True), ('is_sm', '=', True)])
        tot = sum(self.env['account.move.line'].search(
            [('account_id', 'in', fb_accounts.ids),('move_id.state', '=', 'posted'), ('partner_id', 'in', partners.ids),('branch_id', '=', docs.branch_id.id),
             ('date', '=', date)]).mapped('credit'))
        return tot

    def workdays(self, d, end):
        days = []
        excluded = [7]
        while d <= end:
            if d.isoweekday() not in excluded:
                days.append(d)
            d += datetime.timedelta(days=1)
        return days

    def get_working_days(self):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        days = self.workdays(docs.date_from, docs.date_to)
        print(len(days))
        return len(days)

    def get_open_balance(self):
        print('dd')
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        fb_accounts = self.env['account.account'].search(['|', ('is_bank', '=', True), ('is_sm', '=', True)])
        recs = self.env['account.move.line'].search(
            [('account_id', 'in', fb_accounts.ids), ('move_id.state', '=', 'posted'),
             ('branch_id', '=', docs.branch_id.id), ('move_id.is_inter_branch_transfer', '=', False),
             ('date', '<', docs.date_from)])
        tot = 0
        for rec in recs:
            tot = tot + (rec.debit - rec.credit)
        return tot

    @api.model
    def _get_report_values(self, docids, data=None):
        accounts = self.env['account.account'].search([('seq_no', '>', 0), ('is_other_expense', '=', False)], order='seq_no asc')
        other_expense_accounts = self.env['account.account'].search([('seq_no', '>', 0), ('is_other_expense', '=', True)], order='seq_no asc')
        move_lines = self.env['account.move.line'].search([('move_id.branch_id', '=', data["form"]['branch_id'][0]), ('account_id', 'in', accounts.ids), ('move_id.state', '=', 'posted'),('date', '>=', data["form"]['date_from']), ('date', '<=', data["form"]['date_to'])], order='date asc')
        dates = move_lines.mapped('date')
        dates = list(dict.fromkeys(dates))
        return {
            'doc_ids': docids,
            'doc_model': 'menu.report1',
            'data': data['form'],
            'accounts': accounts,
            'other_expense_accounts': other_expense_accounts,
            # 'fb_accounts': fb_accounts,
            'dates': dates,
            'get_date_data': self.get_date_data,
            'get_account_total': self.get_account_total,
            'get_fp_account_total': self.get_fp_account_total,
            'get_bank_account_total': self.get_bank_account_total,
            'get_sm_account_total': self.get_sm_account_total,
            'get_total_sale': self.get_total_sale,
            'get_total_sale_return': self.get_total_sale_return,
            'get_total_purchases': self.get_total_purchases,
            'get_working_days': self.get_working_days,
            'get_open_balance': self.get_open_balance,
        }
