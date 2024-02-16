from odoo import api, fields, models, _

class WizardReportPayslip(models.TransientModel):
    _name = 'wizard.report.payslip'

    date_to = fields.Date('End Date')
    date_from = fields.Date('Start Date')

    def print_payslip(self):
        print("AAA")
        self.ensure_one()
        [data] = self.read()
        payslips = self.env['hr.payslip'].search([
            ('date_from', '>=', self.date_from),
            ('date_to', '<=', self.date_to)])
        datas = {
            'ids': [],
            'model': 'hr.payslip',
            'form': data
        }
        return self.env.ref('tangguh_hr.action_report_payslip').report_action(payslips, data=datas)