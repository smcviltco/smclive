from odoo import models, fields


class ExpenseStatement(models.TransientModel):
    _name = 'expense.statement'

    date_to = fields.Date(string='Date To')
    date_from = fields.Date(string='Date From')
    branch_id = fields.Many2one('res.branch')

    def expense_state_action(self):
        data = {
            'form': self.read()[0],
        }
        return self.env.ref('expense_statement.action_expense_repo').report_action(self, data=data)



