from odoo import api, fields, models
from datetime import datetime, timedelta, time

class HrPayslip(models.Model):

    _inherit = "hr.payslip"

    @api.multi
    def compute_sheet(self):
        result = super(HrPayslip, self).compute_sheet()
        time_from = datetime.combine(self.date_from, time(0, 0, 0))
        time_to = datetime.combine(self.date_to, time(23, 59, 59))
        attendances = self.env['hr.attendance'].search([
            ('employee_id', '=', self.employee_id.id),
            ('check_in', '>=', time_from),
            ('check_out', '<=', time_to)]
        )
        days = (len(attendances.filtered(lambda x: x.total_working_hour >= 8)) + (len(attendances.filtered(lambda x: x.total_working_hour < 8))) * 0.5) or 0
        basic = self.env.ref('hr_payroll.BASIC')
        allowance = self.env.ref('hr_payroll.ALW')
        for work_days in self.worked_days_line_ids:
            work_days.number_of_days = days

        for line in self.line_ids.filtered(lambda x: x.category_id == basic or x.category_id == allowance):
            line.quantity = days

        return result