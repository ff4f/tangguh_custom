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
        days = sum(attendances.mapped('total_days'))
        basic = self.env.ref('hr_payroll.BASIC')
        allowance = self.env.ref('hr_payroll.ALW')
        for work_days in self.worked_days_line_ids:
            work_days.number_of_days = days

        for line in self.line_ids.filtered(lambda x: x.category_id == basic or x.category_id == allowance):
            if line.category_id == basic:
                if line.salary_rule_id.type_allowance == 'basic':
                    line.quantity = (sum(attendances.mapped('one_five')) * 1.5) + (sum(attendances.mapped('two')) * 2) + (sum(attendances.mapped('three')) * 3) + (sum(attendances.mapped('four')) * 4)

                else:
                    line.quantity = days

            else:
                if line.salary_rule_id.type_allowance == 'transportation':
                    line.quantity = sum(attendances.mapped('transportation_allowance'))

                elif line.salary_rule_id.type_allowance == 'meal':
                    line.quantity = sum(attendances.mapped('meal_allowance'))

        return result