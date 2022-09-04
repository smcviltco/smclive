import datetime

from odoo import api, fields, models, _
# from datetime import datetime
from pytz import timezone

class AttendanceReport(models.TransientModel):
    _name = "attendance.report"
    _description = "Attendance Report"

    word_address_id = fields.Many2one('res.partner', string='Work Address')
    date_from = fields.Date()
    date_to = fields.Date()

    def report_pdf_print(self):
        print("click")
        data = {
            'form': self.read()[0],
        }
        return self.env.ref('hr_attendance_report.attendance_report_pdf').report_action(self, data=data)

    def get_attendance(self, d, emp):
        # data = self.env['hr.attendance'].search([('employee_id', '=', emp.id)]).sorted(key=lambda r: r.timestamp)
        data = self.env['hr.attendance'].search([('employee_id', '=', emp.id)])
        boool = 'A'
        if not data and d[1] == 'Sun':
            boool = '-'

        for rec in data:

            if d[2] <= datetime.datetime.today().date() and d[1] != 'Sun':
                if rec.check_in.date() == d[2]:
                    if rec.employee_id.shift_id:
                        if rec.check_in:
                            shift_in = datetime.timedelta(hours=rec.employee_id.shift_id.check_in)
                            shift_in = (datetime.datetime.min + shift_in).time()
                            check_in = rec.check_in.astimezone(timezone('Asia/Karachi')).time()
                            if check_in:
                                boool = 'P'
                            if check_in > shift_in:
                                boool = 'L'
                        if rec.check_out:
                            shift_out = datetime.timedelta(hours=rec.employee_id.shift_id.check_out)
                            shift_out = (datetime.datetime.min + shift_out).time()
                            check_out = rec.check_out.astimezone(timezone('Asia/Karachi')).time()
                            if shift_out:
                                boool = 'P'
                            if check_out < shift_out:
                                boool = 'E'
                        if rec.check_in and rec.check_out:
                            shift_in = datetime.timedelta(hours=rec.employee_id.shift_id.check_in)
                            shift_out = datetime.timedelta(hours=rec.employee_id.shift_id.check_out)
                            shift_in = (datetime.datetime.min + shift_in).time()
                            shift_out = (datetime.datetime.min + shift_out).time()
                            check_in = rec.check_in.astimezone(timezone('Asia/Karachi')).time()
                            check_out = rec.check_out.astimezone(timezone('Asia/Karachi')).time()
                            if check_in > shift_in and check_out < shift_out:
                                boool = 'LE'
            else:
                boool = ' - '
        return boool

