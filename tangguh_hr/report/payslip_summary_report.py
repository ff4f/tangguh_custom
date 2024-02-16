import calendar

from datetime import timedelta
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PayslipSummaryReport(models.AbstractModel):
    _name = 'report.tangguh_hr.report_report_payslip'
    _description = 'Payslip Summary Report'

    def _header_calculate_pay(self):
        res = ['Gaji Pokok', 'Gaji Basic', 'Jam Lembur', 'Uang Lembur', 'Total Upah']
        return res

    def _header_allowance_pay(self):
        res = ['Uang Makan', 'Uang Transport']
        return res

    def _header_deduction_pay(self):
        res = ['Iuran BPJS Kesehatan', 'Iuran BPJS Ketenagakerjaan', 'Pinjaman', 'Total Potongan']
        return res

    def _get_data_from_report(self, data):
        res = []
        payslips = self.env['hr.payslip'].search([('date_from', '>=', data.get('date_from')),
            ('date_to', '<=', data.get('date_to'))])
        for payslip in payslips:
            gaji_basic = sum(payslip.line_ids.filtered(lambda x: x.name == 'Gaji Basic').mapped('total'))
            uang_lembur = sum(payslip.line_ids.filtered(lambda x: x.name == 'Uang Lembur').mapped('total'))
            total_upah = gaji_basic + uang_lembur

            uang_makan = sum(payslip.line_ids.filtered(lambda x: x.name == 'Uang Makan').mapped('total'))
            uang_transportasi = sum(payslip.line_ids.filtered(lambda x: x.name == 'Uang Transport').mapped('total'))
            total_allowance = uang_makan + uang_transportasi + total_upah

            bpjs_kes = sum(payslip.line_ids.filtered(lambda x: x.name == 'BPJS Kesehatan').mapped('total'))
            bpjs_ket = sum(payslip.line_ids.filtered(lambda x: x.name == 'BPJS Ketenagakerjaan').mapped('total'))
            loan = sum(payslip.line_ids.filtered(lambda x: x.name == 'Salary Advance' or x.name == 'Advance Salary' or x.name == 'Pinjaman Karyawan').mapped('total'))
            total_pot = bpjs_kes + bpjs_ket + loan

            net = total_allowance - total_pot
            res.append({
                'name': payslip.employee_id.display_name,
                'position': payslip.employee_id.job_id.display_name,
                'status': payslip.contract_id.payroll_tax.display_name,
                'basic': payslip.contract_id.wage,
                'gaji_pokok': '-',
                'gaji_basic': gaji_basic,
                'jam_lembur': sum(payslip.line_ids.filtered(lambda x: x.name == 'Uang Lembur').mapped('quantity')),
                'uang_lembur': uang_lembur,
                'total_upah': total_upah,
                'uang_transportasi': uang_transportasi,
                'uang_makan': uang_makan,
                'total_allowance': total_allowance,
                'bpjs_kes': bpjs_kes,
                'bpjs_ket': bpjs_ket,
                'loan': loan,
                'total_pot': total_pot,
                'net': net,
                'net_round': round(net, -2),
                'tjk': sum(payslip.line_ids.filtered(lambda x: x.name == 'Gaji Basic').mapped('quantity')) * 8
            })
        return res

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form'):
            raise UserError(_("Form content is missing, this report cannot be printed."))

        payslip_report = self.env['ir.actions.report']._get_report_from_name('tangguh_hr.report_report_payslip')
        payslips = self.env['hr.payslip'].browse(self.ids)
        return {
            'doc_ids': self.ids,
            'doc_model': payslip_report.model,
            'docs': payslips,
            'get_header_calculate_pay': self._header_calculate_pay(),
            'get_header_allowance_pay': self._header_allowance_pay(),
            'get_header_deduction_pay': self._header_deduction_pay(),
            'get_data_from_report': self._get_data_from_report(data['form']),
        }