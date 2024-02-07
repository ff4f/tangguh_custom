import time
from datetime import datetime
from odoo import fields, models, api, _
from odoo.exceptions import except_orm, UserError
from odoo import exceptions


class SalaryAdvancePayment(models.Model):
    _inherit = "salary.advance"

    def check_existing_loan(self):
        if not self.employee_id.address_home_id:
            raise UserError(_('Define home address for employee'))
        salary_advance_search = self.search([('employee_id', '=', self.employee_id.id), ('id', '!=', self.id),
                                             ('state', '=', 'submit')])
        current_month = datetime.strptime(str(self.date), '%Y-%m-%d').date().month
        for each_advance in salary_advance_search:
            existing_month = datetime.strptime(str(each_advance.date), '%Y-%m-%d').date().month
            if current_month == existing_month:
                raise UserError(_('Error!', 'Advance can be requested once in a month'))
        if not self.employee_contract_id:
            raise UserError(_('Define a contract for the employee'))
        struct_id = self.employee_contract_id.struct_id
        if not struct_id.max_percent or not struct_id.advance_date:
            raise UserError(_('Max percentage or advance days are not provided in Contract'))
        adv = self.advance
        amt = (self.employee_contract_id.struct_id.max_percent * self.employee_contract_id.wage) / 100
        if adv > amt and not self.exceed_condition:
            raise UserError(_('Advance amount is greater than allotted'))

        if not self.advance:
            raise UserError(_('You must Enter the Salary Advance amount'))
        payslip_obj = self.env['hr.payslip'].search([('employee_id', '=', self.employee_id.id),
                                                     ('state', '=', 'done'), ('date_from', '<=', self.date),
                                                     ('date_to', '>=', self.date)])
        if payslip_obj:
            raise UserError(_("This month salary already calculated"))

        for slip in self.env['hr.payslip'].search([('employee_id', '=', self.employee_id.id)]):
            slip_moth = datetime.strptime(str(slip.date_from), '%Y-%m-%d').date().month
            if current_month == slip_moth + 1:
                slip_day = datetime.strptime(str(slip.date_from), '%Y-%m-%d').date().day
                current_day = datetime.strptime(str(self.date), '%Y-%m-%d').date().day
                if current_day - slip_day < struct_id.advance_date:
                    raise UserError(
                        _('Request can be done after "%s" Days From prevoius month salary') % struct_id.advance_date)


    @api.one
    def submit_to_manager(self):
        # self.check_existing_loan()
        return super(SalaryAdvancePayment, self).submit_to_manager()