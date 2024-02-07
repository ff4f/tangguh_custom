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
        gross = self.env.ref('hr_payroll.GROSS')
        net = self.env.ref('hr_payroll.NET')
        deduction = self.env.ref('hr_payroll.DED')
        for work_days in self.worked_days_line_ids:
            work_days.number_of_days = days

        salary_advance = self.env['salary.advance'].search(
            [('employee_id', '=', self.employee_id.id), ('state', '=', 'submit'), ('date', '>=', self.date_from),
             ('date', '<=', self.date_to)])

        loan = 0

        if salary_advance:
            if self.input_line_ids.filtered(lambda x: x.name == 'Salary Advance'):
                for input in self.input_line_ids.filtered(lambda x: x.name == 'Salary Advance'):
                    input.write({'amount': sum(salary_advance.mapped('advance'))})
            else:
                self.input_line_ids = [(0, 0, {
                    'name': 'Salary Advance',
                    'contract_id': self.contract_id.id,
                    'code': 'SAR',
                    'amount': sum(salary_advance.mapped('advance'))
                })]

            loan = sum(salary_advance.mapped('advance'))

        for line in self.line_ids.filtered(lambda x: x.name == 'Salary Advance' or x.name == 'Advance Salary'):
            line.amount = loan


        total = 0
        total_ded = 0
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
            total += line.total

        for line in self.line_ids.filtered(lambda x: x.category_id == gross):
            line.amount = total

        for line in self.line_ids.filtered(lambda x: x.category_id == deduction):
            total_ded += line.total

        total_net = total - total_ded

        for line in self.line_ids.filtered(lambda x: x.category_id == net):
            line.amount = total_net

        return result