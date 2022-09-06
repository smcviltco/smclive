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

    @api.model
    def _get_report_values(self, docids, data=None):
        accounts = self.env['account.account'].search([('seq_no', '>', 0)], order='seq_no asc')
        move_lines = self.env['account.move.line'].search([('move_id.branch_id', '=', data["form"]['branch_id'][0]), ('account_id', 'in', accounts.ids), ('date', '>=', data["form"]['date_from']), ('date', '<=', data["form"]['date_to'])], order='')
        dates = move_lines.mapped('date')
        dates = list(dict.fromkeys(dates))
        return {
            'doc_ids': docids,
            'doc_model': 'menu.report1',
            'data': data['form'],
            'accounts': accounts,
            'dates': dates,
            'get_date_data': self.get_date_data,
        }
