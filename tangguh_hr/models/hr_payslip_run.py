from odoo import api, fields, models
from datetime import datetime, timedelta, time

class HrPayslipRun(models.Model):

    _inherit = "hr.payslip.run"

    @api.multi
    def print_quotation(self):
        return self.env.ref('tangguh_hr.action_report_payslip')\
            .with_context(discard_logo_check=True).report_action(self)

    def _generate_slip_value(self):
        res = []

        for payslips in self.slip_ids:
            for payslip in payslips:
                gaji_basic = sum(payslip.line_ids.filtered(lambda x: x.name == 'Gaji Basic').mapped('total'))
                uang_lembur = sum(payslip.line_ids.filtered(lambda x: x.name == 'Uang Lembur').mapped('total'))
                total_upah = gaji_basic + uang_lembur

                uang_makan = sum(payslip.line_ids.filtered(lambda x: x.name == 'Uang Makan').mapped('total'))
                uang_transportasi = sum(payslip.line_ids.filtered(lambda x: x.name == 'Uang Transport').mapped('total'))
                total_allowance = uang_makan + uang_transportasi + total_upah

                bpjs_kes = sum(payslip.line_ids.filtered(lambda x: x.name == 'BPJS Kesehatan').mapped('total'))
                bpjs_ket = sum(payslip.line_ids.filtered(lambda x: x.name == 'BPJS Ketenagakerjaan').mapped('total'))
                loan = sum(payslip.line_ids.filtered(lambda
                                                         x: x.name == 'Salary Advance' or x.name == 'Advance Salary' or x.name == 'Pinjaman Karyawan').mapped(
                    'total'))
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