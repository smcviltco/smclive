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
            [('account_id', '=', account.id),('move_id.state', '=', 'posted'), ('move_id.branch_id', '=', docs.branch_id.id),('move_id.is_salary', '=', False),
             ('date', '=', date)]).mapped('debit'))
        return tot

    def get_account_total(self, account):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        tot = sum(self.env['account.move.line'].search(
            [('account_id', '=', account.id), ('move_id.branch_id', '=', docs.branch_id.id),('move_id.is_salary', '=', False),
             ('date', '>=', docs.date_from),('move_id.state', '=', 'posted'), ('date', '<=', docs.date_to)]).mapped('debit'))
        return tot

    def get_fp_account_total(self):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        fb_accounts = self.env['account.account'].search([('is_fp', '=', True)])
        tot = sum(self.env['account.move.line'].search(
            [('account_id', 'in', fb_accounts.ids),('move_id.state', '=', 'posted'), ('move_id.branch_id', '=', docs.branch_id.id),
             ('date', '>=', docs.date_from), ('date', '<=', docs.date_to)]).mapped('debit'))
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
        return len(days)

    def get_open_balance(self):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        fb_accounts = self.env['account.account'].search(['|', ('is_bank', '=', True), ('is_sm', '=', True)])
        recs = self.env['account.move.line'].search(
            [('account_id', 'in', fb_accounts.ids), ('move_id.state', '=', 'posted'),
             ('branch_id', '=', docs.branch_id.id),
             ('date', '<', docs.date_from)])
        tot = 0
        for rec in recs:
            tot = tot + (rec.debit - rec.credit)
        return tot

    def get_open_balance_cashin(self):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        fb_accounts = self.env['account.account'].search([('id', '=', 371)])
        recs = self.env['account.move.line'].search(
            [('account_id', 'in', fb_accounts.ids), ('move_id.state', '=', 'posted'),

             ('date', '<', docs.date_from)])
        tot = 0
        for rec in recs:
            tot = tot + (rec.debit - rec.credit)
        return tot

    def get_construction_balance(self):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        fb_accounts = self.env['account.account'].search(['|',('user_type_id.name', '=', "Expenses"),('internal_type', '=', 'payable')])
        partners = self.env['res.partner'].search([('partner_type', '=', "construction")])
        vals = []
        for partner in partners:
            tot = sum(self.env['account.move.line'].search(
                [('account_id', 'in', fb_accounts.ids),('partner_id', '=', partner.id), ('move_id.state', '=', 'posted'),
                 ('move_id.branch_id', '=', docs.branch_id.id),
                 ('date', '>=', docs.date_from), ('date', '<=', docs.date_to)]).mapped('debit'))
            if tot:
                vals.append({
                    'partner_name': partner.name,
                    'amount': tot,
                })
        return vals

    # def get_sm_balance(self):
    #     model = self.env.context.get('active_model')
    #     docs = self.env[model].browse(self.env.context.get('active_id'))
    #     fb_accounts = self.env['account.account'].search([('is_head_office', '=', True)])
    #     tot = sum(self.env['account.move.line'].search(
    #         [('account_id', 'in', fb_accounts.ids), ('move_id.state', '=', 'posted'),
    #          ('move_id.branch_id', '=', docs.branch_id.id),
    #          ('date', '>=', docs.date_from), ('date', '<=', docs.date_to)]).mapped('debit'))
    #     print()
    #     # tot = 0
    #     # for rec in recs:
    #     #     tot = tot + (rec.debit - rec.credit)
    #     print(tot)
    #     return tot clearing_accounts

    def get_cash_account(self):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        fb_accounts = self.env['account.account'].search([('is_sm', '=', True)])
        vals = []
        for account in fb_accounts:
            tot = sum(self.env['account.move.line'].search(
                [('account_id', '=', account.id), ('move_id.state', '=', 'posted'), ('account_id.statements_branch', '!=', docs.branch_id.id),
                 ('move_id.branch_id', '=', docs.branch_id.id),
                 ('date', '>=', docs.date_from), ('date', '<=', docs.date_to)]).mapped('debit'))
            if tot:
                vals.append({
                    'account_name': account.name,
                    'amount': tot,
                })
        return vals

    def get_clearing_account(self):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        move_lines = self.env['account.move.line'].search(
            [('payment_id.is_expense', '=', True), ('move_id.state', '=', 'posted'),
             ('move_id.branch_id', '=', docs.branch_id.id),
             ('date', '>=', docs.date_from), ('date', '<=', docs.date_to)])
        partners = move_lines.mapped('payment_id.partner_id')
        vals = []
        for partner in partners:
            tot = sum(self.env['account.move.line'].search(
                [('payment_id.partner_id', '=', partner.id), ('move_id.state', '=', 'posted'), ('payment_id.is_expense', '=', True),
                 ('move_id.branch_id', '=', docs.branch_id.id),
                 ('date', '>=', docs.date_from), ('date', '<=', docs.date_to)]).mapped('debit'))
            if tot:
                vals.append({
                    'partner_name': partner.name,
                    'amount': tot,
                })
        return vals

    def get_bank_balance(self):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        fb_accounts = self.env['account.account'].search([('is_bank', '=', True)])

        tot = sum(self.env['account.move.line'].search(
            [('account_id', 'in', fb_accounts.ids),('move_id.state', '=', 'posted'),('move_id.branch_id', '=', docs.branch_id.id),
             ('date', '>=', docs.date_from), ('date', '<=', docs.date_to)]).mapped('debit'))
        return tot

    def get_inter_branch_balance(self):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        # fb_accounts = self.env['account.account'].search([('is_bank', '=', True)])

        tot_receive = sum(self.env['account.move.line'].search(
            [('move_id.is_inter_branch_transfer', '=', True),('move_id.state', '=', 'posted'),('branch_id', '=', docs.branch_id.id),
             ('date', '>=', docs.date_from), ('date', '<=', docs.date_to)]).mapped('debit'))
        tot_paid = sum(self.env['account.move.line'].search(
            [('move_id.is_inter_branch_transfer', '=', True),('move_id.state', '=', 'posted'),('branch_id', '=', docs.branch_id.id),
             ('date', '>=', docs.date_from), ('date', '<=', docs.date_to)]).mapped('credit'))
        return tot_receive, tot_paid

    def cashin_accounts(self):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        move_lines = self.env['account.move.line'].search(
            [('account_id', '=', 371), ('move_id.state', '=', 'posted'),('debit', '!=', 0),
             ('date', '>=', docs.date_from), ('date', '<=', docs.date_to)])
        moves = move_lines.mapped('move_id').ids
        move_lines_credit = self.env['account.move.line'].search(
            [('move_id.state', '=', 'posted'), ('move_id', 'in', moves),('credit', '!=', 0),
             ('date', '>=', docs.date_from), ('date', '<=', docs.date_to)])
        credit_accounts = move_lines_credit.mapped('account_id')
        credit_accounts = credit_accounts.filtered(lambda i:i.internal_type == 'liquidity')
        vals = []
        for account in credit_accounts:
            if account.id != 371:
                tot = sum(self.env['account.move.line'].search(
                [('account_id', '=', account.id), ('move_id.state', '=', 'posted'), ('move_id', 'in', moves),('credit', '!=', 0),
                 ('date', '>=', docs.date_from), ('date', '<=', docs.date_to)]).mapped('credit'))
                if tot:
                    vals.append({
                        'account_name': account.name,
                        'amount': tot,
                    })
        return vals

    def get_cashin_expense_accounts(self):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        move_lines = self.env['account.move.line'].search([('date', '>=', rec_model.date_from),
                                                        ('date', '<=', rec_model.date_to),
                                                        ('move_id.state', '=', 'posted'),
                                                        ('credit', '!=', 0),
                                                        ('account_id', '=', 371),
                                                        ('is_check', '=', False)], order="date asc")
        moves = move_lines.mapped('move_id').ids
        move_lines_debit = self.env['account.move.line'].search(
            [('move_id.state', '=', 'posted'), ('move_id', 'in', moves), ('debit', '!=', 0),('account_id', '!=', 8),
             ('date', '>=', rec_model.date_from), ('date', '<=', rec_model.date_to)])
        debit_accounts = move_lines_debit.mapped('account_id')
        # accounts = self.env['account.move.line'].search(
        #     [('account_id', 'in', debit_accounts.ids), ('move_id.state', '=', 'posted'), ('move_id', 'in', moves),
        #      ('debit', '!=', 0),
        #      ('date', '>=', rec_model.date_from), ('date', '<=', rec_model.date_to)])
        return debit_accounts

    def get_cashin_expense_account(self, account):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        move_lines = self.env['account.move.line'].search([('date', '>=', rec_model.date_from),
                                                           ('date', '<=', rec_model.date_to),
                                                           ('move_id.state', '=', 'posted'),
                                                           ('credit', '!=', 0),
                                                           ('account_id', '=', 371),
                                                           ('is_check', '=', False)], order="date asc")
        moves = move_lines.mapped('move_id').ids

        # move_lines_credit = self.env['account.move.line'].search(
        #     [('move_id.state', '=', 'posted'), ('move_id', 'in', moves), ('credit', '!=', 0),
        #
        #      ('date', '>=', rec_model.date_from), ('date', '<=', rec_model.date_to)])
        # credit_accounts = move_lines_credit.mapped('account_id')
        tot = sum(self.env['account.move.line'].search(
            [('account_id', '=', account.id), ('move_id.state', '=', 'posted'), ('move_id', 'in', moves),
             ('debit', '!=', 0),
             ('date', '>=', rec_model.date_from), ('date', '<=', rec_model.date_to)]).mapped('debit'))
        return tot

    def get_cashin_expense_account_date(self,date, account):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        move_lines = self.env['account.move.line'].search([('date', '>=', rec_model.date_from),
                                                           ('date', '<=', rec_model.date_to),
                                                           ('move_id.state', '=', 'posted'),
                                                           ('credit', '!=', 0),
                                                           ('account_id', '=', 371),
                                                           ('is_check', '=', False)], order="date asc")
        moves = move_lines.mapped('move_id').ids
        # move_lines_credit = self.env['account.move.line'].search(
        #     [('move_id.state', '=', 'posted'), ('move_id', 'in', moves), ('credit', '!=', 0),
        #
        #      ('date', '>=', rec_model.date_from), ('date', '<=', rec_model.date_to)])
        # credit_accounts = move_lines_credit.mapped('account_id')
        tot = sum(self.env['account.move.line'].search(
            [('account_id', '=', account.id), ('move_id.state', '=', 'posted'), ('move_id', 'in', moves),
             ('debit', '!=', 0), ('is_check', '=', False),
             ('date', '=', date)]).mapped('debit'))
        return tot

    def cashin_payable_accounts(self):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        move_lines = self.env['account.move.line'].search([('date', '>=', rec_model.date_from),
                                                           ('date', '<=', rec_model.date_to),
                                                           ('move_id.state', '=', 'posted'),
                                                           ('credit', '!=', 0),
                                                           ('account_id', '=', 371),
                                                           ('is_check', '=', False)], order="date asc")
        moves = move_lines.mapped('move_id').ids
        move_lines_debit = self.env['account.move.line'].search(
            [('move_id.state', '=', 'posted'), ('move_id', 'in', moves), ('debit', '!=', 0),
             ('date', '>=', rec_model.date_from), ('date', '<=', rec_model.date_to)])
        debit_accounts = move_lines_debit.mapped('account_id')
        debit_accounts = debit_accounts.filtered(lambda i: i.internal_type == 'payable')
        vals = []
        # for account in credit_accounts:
        #     if account.id != 371:
        lines = self.env['account.move.line'].search(
        [('account_id', 'in', debit_accounts.ids), ('move_id.state', '=', 'posted'), ('move_id', 'in', moves),
         ('date', '>=', rec_model.date_from), ('date', '<=', rec_model.date_to)])
        for rec in lines:
        # if tot:
            vals.append({
                'partner_id': rec.partner_id.id,
                'partner_name': rec.partner_id.secondary_name,
                'amount': rec.debit,
            })
        return vals

    def cashin_payable_partner(self, date, partner):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        move_lines = self.env['account.move.line'].search([('date', '=', date),
                                                           ('move_id.state', '=', 'posted'),
                                                           ('credit', '!=', 0),
                                                           ('account_id', '=', 371),
                                                           ('is_check', '=', False)], order="date asc")
        moves = move_lines.mapped('move_id').ids
        move_lines_debit = self.env['account.move.line'].search(
            [('move_id.state', '=', 'posted'), ('move_id', 'in', moves), ('debit', '!=', 0),
             ('date', '=', date)])
        debit_accounts = move_lines_debit.mapped('account_id')
        debit_accounts = debit_accounts.filtered(lambda i: i.internal_type == 'payable')
        vals = []
        # for account in credit_accounts:
        #     if account.id != 371:
        lines = self.env['account.move.line'].search(
        [('account_id', 'in', debit_accounts.ids), ('move_id.state', '=', 'posted'), ('move_id', 'in', moves),('partner_id', '=', partner),
         ('date', '=', date)])
        amount = 0
        for rec in lines:
            amount = amount + rec.debit
        # if tot:
        #     vals.append({
        #         'partner_id': rec.partner_id.id,
        #         'partner_name': rec.partner_id.name,
        #         'amount': rec.debit,
        #     })
        return amount

    def cashin_payable_partner_total(self, partner):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        move_lines = self.env['account.move.line'].search([('date', '>=', rec_model.date_from),
                                                        ('date', '<=', rec_model.date_to),
                                                           ('move_id.state', '=', 'posted'),
                                                           ('credit', '!=', 0),
                                                           ('account_id', '=', 371),
                                                           ('is_check', '=', False)], order="date asc")
        moves = move_lines.mapped('move_id').ids
        move_lines_debit = self.env['account.move.line'].search(
            [('move_id.state', '=', 'posted'), ('move_id', 'in', moves), ('debit', '!=', 0),
             ('date', '>=', rec_model.date_from),
             ('date', '<=', rec_model.date_to),])
        debit_accounts = move_lines_debit.mapped('account_id')
        debit_accounts = debit_accounts.filtered(lambda i: i.internal_type == 'payable')
        vals = []
        # for account in credit_accounts:
        #     if account.id != 371:
        lines = self.env['account.move.line'].search(
        [('account_id', 'in', debit_accounts.ids), ('move_id.state', '=', 'posted'), ('move_id', 'in', moves),('partner_id', '=', partner),
         ('date', '>=', rec_model.date_from),
         ('date', '<=', rec_model.date_to),])
        amount = 0
        for rec in lines:
            amount = amount + rec.debit
        # if tot:
        #     vals.append({
        #         'partner_id': rec.partner_id.id,
        #         'partner_name': rec.partner_id.name,
        #         'amount': rec.debit,
        #     })
        return amount

    def get_cashin_expense_accounts_raiwaind(self):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        move_lines = self.env['account.move.line'].search([('date', '>=', rec_model.date_from),
                                                        ('date', '<=', rec_model.date_to),
                                                        ('move_id.state', '=', 'posted'),
                                                        ('account_id', '=', 174),
                                                        ], order="date asc")
        moves = move_lines.mapped('move_id').ids
        move_lines_debit = self.env['account.move.line'].search(
            [('move_id.state', '=', 'posted'), ('move_id', 'in', moves), ('debit', '!=', 0),
             ('date', '>=', rec_model.date_from), ('date', '<=', rec_model.date_to)])
        debit_accounts = move_lines_debit.mapped('account_id')
        # accounts = self.env['account.move.line'].search(
        #     [('account_id', 'in', debit_accounts.ids), ('move_id.state', '=', 'posted'), ('move_id', 'in', moves),
        #      ('debit', '!=', 0),
        #      ('date', '>=', rec_model.date_from), ('date', '<=', rec_model.date_to)])
        return debit_accounts

    def get_cashin_expense_accounts_raiwaind_total(self, account):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        move_lines = self.env['account.move.line'].search([('date', '>=', rec_model.date_from),
                                                           ('date', '<=', rec_model.date_to),
                                                           ('move_id.state', '=', 'posted'),
                                                           ('credit', '!=', 0),
                                                           ('account_id', '=', 174),
                                                           ('is_check', '=', False)], order="date asc")
        moves = move_lines.mapped('move_id').ids

        # move_lines_credit = self.env['account.move.line'].search(
        #     [('move_id.state', '=', 'posted'), ('move_id', 'in', moves), ('credit', '!=', 0),
        #
        #      ('date', '>=', rec_model.date_from), ('date', '<=', rec_model.date_to)])
        # credit_accounts = move_lines_credit.mapped('account_id')
        tot = sum(self.env['account.move.line'].search(
            [('account_id', '=', account.id), ('move_id.state', '=', 'posted'), ('move_id', 'in', moves),
             ('debit', '!=', 0),
             ('date', '>=', rec_model.date_from), ('date', '<=', rec_model.date_to)]).mapped('debit'))
        return tot

    def get_cashin_expense_accounts_raiwaind_date(self,date, account):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        move_lines = self.env['account.move.line'].search([('date', '>=', rec_model.date_from),
                                                           ('date', '<=', rec_model.date_to),
                                                           ('move_id.state', '=', 'posted'),
                                                           ('account_id', '=', 174)], order="date asc")
        moves = move_lines.mapped('move_id').ids
        # move_lines_credit = self.env['account.move.line'].search(
        #     [('move_id.state', '=', 'posted'), ('move_id', 'in', moves), ('credit', '!=', 0),
        #
        #      ('date', '>=', rec_model.date_from), ('date', '<=', rec_model.date_to)])
        # credit_accounts = move_lines_credit.mapped('account_id')
        tot = sum(self.env['account.move.line'].search(
            [('account_id', '=', account.id), ('move_id.state', '=', 'posted'), ('move_id', 'in', moves),
             ('debit', '!=', 0), ('is_check', '=', False),
             ('date', '=', date)]).mapped('debit'))
        return tot

    def get_headoffice_dates(self):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        move_lines = self.env['account.move.line'].search([('date', '>=', rec_model.date_from),
                                                           ('date', '<=', rec_model.date_to),
                                                           ('move_id.state', '=', 'posted'),
                                                           ('account_id', '=', 371)], order="date asc")
        dates = move_lines.mapped('date')
        dates = list(dict.fromkeys(dates))
        return dates

    def get_raiwind_dates(self):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        move_lines = self.env['account.move.line'].search([('date', '>=', rec_model.date_from),
                                                           ('date', '<=', rec_model.date_to),
                                                           ('move_id.state', '=', 'posted'),
                                                           ('account_id', '=', 174)], order="date asc")
        dates = move_lines.mapped('date')
        dates = list(dict.fromkeys(dates))
        return dates

    def get_open_balance_cashin_raiwind(self):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        fb_accounts = self.env['account.account'].search([('id', '=', 174)])
        recs = self.env['account.move.line'].search(
            [('account_id', 'in', fb_accounts.ids), ('move_id.state', '=', 'posted'),

             ('date', '<', docs.date_from)])
        tot = 0
        for rec in recs:
            tot = tot + (rec.debit - rec.credit)
        return tot

    def cashin_accounts_raiwind(self):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        move_lines = self.env['account.move.line'].search(
            [('account_id', '=', 174), ('move_id.state', '=', 'posted'),('debit', '!=', 0),
             ('date', '>=', docs.date_from), ('date', '<=', docs.date_to)])
        moves = move_lines.mapped('move_id').ids
        move_lines_credit = self.env['account.move.line'].search(
            [('move_id.state', '=', 'posted'), ('move_id', 'in', moves),('credit', '!=', 0),
             ('date', '>=', docs.date_from), ('date', '<=', docs.date_to)])
        credit_accounts = move_lines_credit.mapped('account_id')
        credit_accounts = credit_accounts.filtered(lambda i: i.internal_type in ['liquidity', 'other'])
        vals = []
        for account in credit_accounts:
            if account.id != 174:
                tot = sum(self.env['account.move.line'].search(
                [('account_id', '=', account.id), ('move_id.state', '=', 'posted'), ('move_id', 'in', moves),('credit', '!=', 0),
                 ('date', '>=', docs.date_from), ('date', '<=', docs.date_to)]).mapped('credit'))
                if tot:
                    vals.append({
                        'account_name': account.name,
                        'amount': tot,
                    })
        return vals

    @api.model
    def _get_report_values(self, docids, data=None):
        accounts = self.env['account.account'].search([('seq_no', '>', 0), '|', ('is_other_expense', '=', False), ('is_salary_expense', '=', True)], order='seq_no asc')
        other_expense_accounts = self.env['account.account'].search([('seq_no', '>', 0), ('is_other_expense', '=', True)], order='seq_no asc')
        move_lines = self.env['account.move.line'].search([('move_id.branch_id', '=', data["form"]['branch_id'][0]), ('account_id', 'in', accounts.ids), ('move_id.is_salary', '=', False),('move_id.state', '=', 'posted'),('date', '>=', data["form"]['date_from']), ('date', '<=', data["form"]['date_to'])], order='date asc')
        dates = move_lines.mapped('date')
        dates = list(dict.fromkeys(dates))
        print(dates)
        # print(data['form']['branch_id'])
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
            'get_open_balance_cashin': self.get_open_balance_cashin,
            'get_construction_balance': self.get_construction_balance,
            # 'get_sm_balance': self.get_sm_balance,
            'get_cash_account': self.get_cash_account,
            'get_clearing_account': self.get_clearing_account,
            'get_bank_balance': self.get_bank_balance,
            'get_inter_branch_balance': self.get_inter_branch_balance,
            'cashin_accounts': self.cashin_accounts,
            'get_cashin_expense_accounts': self.get_cashin_expense_accounts,
            'get_cashin_expense_account': self.get_cashin_expense_account,
            'get_cashin_expense_account_date': self.get_cashin_expense_account_date,
            'cashin_payable_accounts': self.cashin_payable_accounts,
            'cashin_payable_partner': self.cashin_payable_partner,
            'cashin_payable_partner_total': self.cashin_payable_partner_total,


            'get_open_balance_cashin_raiwind': self.get_open_balance_cashin_raiwind,
            'cashin_accounts_raiwind': self.cashin_accounts_raiwind,
            'get_headoffice_dates': self.get_headoffice_dates,
            'get_raiwind_dates': self.get_raiwind_dates,
            'get_cashin_expense_accounts_raiwaind': self.get_cashin_expense_accounts_raiwaind,
            'get_cashin_expense_accounts_raiwaind_total': self.get_cashin_expense_accounts_raiwaind_total,
            'get_cashin_expense_accounts_raiwaind_date': self.get_cashin_expense_accounts_raiwaind_date,


        }
