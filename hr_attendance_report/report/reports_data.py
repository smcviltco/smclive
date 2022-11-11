from odoo import models, api
from datetime import timedelta, datetime
from itertools import groupby

from odoo.exceptions import UserError


class EmpReport(models.AbstractModel):
    _name = 'report.hr_attendance_report.attendance_report_id_print'
    _description = 'Attendance Report'

    def get_days(self, result):
        delta = result.date_to - result.date_from  # returns timedelta
        days = []
        for i in range(delta.days + 1):
            diff = result.date_from + timedelta(days=i)
            days.append([diff.day, diff.strftime('%a'), diff])
        return days

    @api.model
    def _get_report_values(self, docids, data=None):
        result = self.env['attendance.report'].browse(self.env.context.get('active_ids'))
        day = result.date_to - result.date_from
        if day.days + 1 > 31:
            raise UserError('Date Ranges should be less than 30 days.')
        d = self.env['user.attendance'].search([])
        for x in d:
            x.address_id = x.employee_id.address_id
            x.department_id = x.employee_id.department_id.id
        data = self.env['user.attendance'].search([('employee_id.address_id', '=', result.word_address_id.id)]).sorted(
            key=lambda r: r.timestamp)
        emp = []
        for rec in data:
            emp.append(rec.employee_id.id)
        emp = list(dict.fromkeys(emp))
        up_days = self.get_days(result)
        employees = self.env['hr.employee'].search([('id', 'in', emp)])
        return {
            'doc_ids': docids,
            'doc_model': 'attendance.report',
            'date_wizard': result,
            'data': data,
            'employees': employees,
            'departments': data.mapped('department_id'),
            'days': up_days,
            'cols': len(up_days) + 7,
            # 'get_attendance': self.get_attendance(day),
        }
