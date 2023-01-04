# -*- coding: utf-8 -*-

from odoo import models, api, fields, models, _
from odoo.tools import float_compare, float_is_zero
from odoo.exceptions import UserError, ValidationError
from datetime import datetime


class AccountMoveInh(models.Model):
    _inherit = 'account.move'

    is_salary = fields.Boolean()


class HrEmployeeInh(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def create(self, vals):
        rec = super(HrEmployeeInh, self).create(vals)
        record = self.env['res.partner'].create({
            'name': vals['name'],
            'partner_type': 'employee',
            'is_employee': True,
        })
        record_current = self.env['res.partner'].create({
            'name': vals['name']+'- Current Advance',
            'is_current': True,
            'partner_type': 'employee',
            'is_employee': True,
        })
        record_old = self.env['res.partner'].create({
            'name': vals['name'] + '- Old Advance',
            'partner_type': 'employee',
            'is_employee': True,
        })
        records = [record_current.id, record_old.id]
        rec.address_home_id = record
        rec.partner_ids = records
        return rec


class HrPayslipInh(models.Model):
    _inherit = 'hr.payslip'

    # def create_update_jv(self):
    #     payslips = self.env['hr.payslip'].search([])
    #     for s in payslips:
    #         s.move_id.is_salary = True

    def action_payslip_done(self):
        record = super(HrPayslipInh, self).action_payslip_done()
        self._action_general_entry()
        for rec in self:
            new_partner = ''
            old_partner = ''
            if rec.employee_id.partner_ids:
                for partner in rec.employee_id.partner_ids:
                    if partner.is_current:
                        new_partner = partner.id
                    if not partner.is_current:
                        old_partner = partner.id
            for line in rec.move_id.line_ids:
                if line.account_id.is_new:
                    line.partner_id = new_partner
                if line.account_id.is_old:
                    line.partner_id = old_partner
        return record

    def _action_general_entry(self):
        line_ids = []
        debit_sum = 0.0
        credit_sum = 0.0
        for rec in self:
            if rec.employee_id.partner_ids:
                current = -1
                old = -1
                for p in rec.employee_id.partner_ids:
                    if not p.is_current:
                        old = p
                    else:
                        current = p
                if old != -1 and current != -1:
                    move_dict = {
                        'ref': rec.number,
                        'is_salary': True,
                        'journal_id': rec.journal_id.id,
                        'address_id': rec.address_id.id,
                        # 'partner_id': rec.employee_id.address_home_id.id,
                        'date': datetime.today(),
                        'state': 'draft',
                    }
                    for oline in rec.line_ids:
                        if oline.salary_rule_id.account_debit and oline.salary_rule_id.account_credit and oline.total > 0:
                            if oline.code == 'OAD':
                                partner = old
                            elif oline.code == 'CAD':
                                partner = current
                            else:
                                partner = rec.employee_id.address_home_id
                            debit_line = (0, 0, {
                                'name': oline.name,
                                'debit': abs(oline.total),
                                'credit': 0.0,
                                'partner_id': partner.id,
                                'account_id': oline.salary_rule_id.account_debit.id,
                            })
                            line_ids.append(debit_line)
                            debit_sum += debit_line[2]['debit'] - debit_line[2]['credit']
                            credit_line = (0, 0, {
                                'name': oline.name,
                                'debit': 0.0,
                                'partner_id': partner.id,
                                'credit': abs(oline.total),
                                'account_id': oline.salary_rule_id.account_credit.id,
                            })
                            line_ids.append(credit_line)
                            credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']
                    if line_ids:
                        move_dict['line_ids'] = line_ids
                        move = self.env['account.move'].create(move_dict)
                        line_ids = []
                        rec.move_id = move.id
                        print("General entry created")