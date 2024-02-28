from odoo import api, fields, models
from datetime import datetime, timedelta, time
# import locale
#
# locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')

nama_hari = {
    0: 'Minggu',
    1: 'Senin',
    2: 'Selasa',
    3: 'Rabu',
    4: 'Kamis',
    5: 'Jumat',
    6: 'Sabtu'
}

class HrPayslip(models.Model):

    _inherit = "hr.payslip"

    def _get_employee_attendance(self):
        res = []
        time_from = datetime.combine(self.date_from, time(0, 0, 0))
        time_to = datetime.combine(self.date_to, time(23, 59, 59))
        attendances = self.env['hr.attendance'].search([
            ('employee_id', '=', self.employee_id.id),
            ('check_in', '>=', time_from),
            ('check_out', '<=', time_to)],
            order='check_in asc'
        )

        for attendace in attendances:
            check_in = attendace.check_in +timedelta(hours=7)
            check_out = attendace.check_out +timedelta(hours=7)

            indeks_hari = check_in.weekday()
            if attendace.total_working_hour >= 8:
                gb = 1
            elif  attendace.total_working_hour < 8 and attendace.total_working_hour >= 1:
                gb = 0.5
            else:
                gb = 0

            res.append({
                'tanggal_masuk': check_in.strftime('%d-%m-%Y'),
                'hari': nama_hari[indeks_hari],
                'jam_masuk': check_in.strftime('%H:%M'),
                'jam_keluar': check_out.strftime('%H:%M'),
                'tjk': attendace.total_working_hour,
                'njk': attendace.normally_working_hour,
                'gb': gb,
                'gp': '-',
                '1,5': attendace.one_five,
                '2': attendace.two,
                '3': attendace.three,
                '4': attendace.four,
                'uang_makan': attendace.meal_allowance,
                'uang_transport': attendace.transportation_allowance,
            })

        return res

    def _compute_total_hour(self):
        time_from = datetime.combine(self.date_from, time(0, 0, 0))
        time_to = datetime.combine(self.date_to, time(23, 59, 59))
        attendances = self.env['hr.attendance'].search([
            ('employee_id', '=', self.employee_id.id),
            ('check_in', '>=', time_from),
            ('check_out', '<=', time_to)]
        )
        gb_tot = 0

        for attendace in attendances:
            if attendace.total_working_hour >= 8:
                gb = 1
            elif  attendace.total_working_hour < 8 and attendace.total_working_hour >= 1:
                gb = 0.5
            else:
                gb = 0
            gb_tot += gb

        tjk = sum(attendances.mapped('total_working_hour'))
        njk = sum(attendances.mapped('normally_working_hour'))
        gp = '-'
        one_five = sum(attendances.mapped('one_five'))
        two = sum(attendances.mapped('one_five'))
        three = sum(attendances.mapped('three'))
        four = sum(attendances.mapped('four'))
        uang_makan = sum(attendances.mapped('meal_allowance'))
        uang_transport = sum(attendances.mapped('transportation_allowance'))
        total_lembur = (one_five * 1.5) + (two * 2) + (three * 3) + (four * 4)

        return tjk, njk, gb_tot, gp, one_five, two, three, four, uang_makan, uang_transport, total_lembur



    @api.multi
    def compute_sheet(self):
        result = super(HrPayslip, self).compute_sheet()
        for line in self:
            time_from = datetime.combine(line.date_from, time(0, 0, 0))
            time_to = datetime.combine(line.date_to, time(23, 59, 59))
            attendances = line.env['hr.attendance'].search([
                ('employee_id', '=', line.employee_id.id),
                ('check_in', '>=', time_from),
                ('check_out', '<=', time_to)]
            )
            days = sum(attendances.mapped('total_days'))
            basic = line.env.ref('hr_payroll.BASIC')
            allowance = line.env.ref('hr_payroll.ALW')
            gross = line.env.ref('hr_payroll.GROSS')
            net = line.env.ref('hr_payroll.NET')
            deduction = line.env.ref('hr_payroll.DED')
            tax = line.env.ref('tangguh_hr.TAX')
            for work_days in line.worked_days_line_ids:
                work_days.number_of_days = days

            salary_advance = line.env['salary.advance'].search(
                [('employee_id', '=', line.employee_id.id), ('state', '=', 'submit'), ('date', '>=', line.date_from),
                 ('date', '<=', line.date_to)])

            loan = 0

            if salary_advance:
                if line.input_line_ids.filtered(lambda x: x.name == 'Salary Advance'):
                    for input in line.input_line_ids.filtered(lambda x: x.name == 'Salary Advance'):
                        input.write({'amount': -sum(salary_advance.mapped('advance'))})
                else:
                    line.input_line_ids = [(0, 0, {
                        'name': 'Salary Advance',
                        'contract_id': line.contract_id.id,
                        'code': 'SAR',
                        'amount': -sum(salary_advance.mapped('advance'))
                    })]

                loan = sum(salary_advance.mapped('advance'))

            for record in line.line_ids.filtered(lambda x: x.name == 'Salary Advance' or x.name == 'Advance Salary' or x.name == 'Pinjaman Karyawan'):
                record.amount = loan


            total = 0
            total_ded = 0
            for record in line.line_ids.filtered(lambda x: x.category_id == basic or x.category_id == allowance):
                if record.category_id == basic:
                    if record.salary_rule_id.type_allowance == 'basic':
                        record.quantity = (sum(attendances.mapped('one_five')) * 1.5) + (sum(attendances.mapped('two')) * 2) + (sum(attendances.mapped('three')) * 3) + (sum(attendances.mapped('four')) * 4)

                    else:
                        record.quantity = days

                else:
                    if record.salary_rule_id.type_allowance == 'transportation':
                        record.quantity = sum(attendances.mapped('transportation_allowance'))

                    elif record.salary_rule_id.type_allowance == 'meal':
                        record.quantity = sum(attendances.mapped('meal_allowance'))
                total += record.total

            for record in line.line_ids.filtered(lambda x: x.category_id == gross):
                record.amount = total

            for record in line.line_ids.filtered(lambda x: x.category_id == deduction):
                total_ded += record.total

            for record in line.line_ids.filtered(lambda x: x.name == 'Total Potongan'):
                record.amount = total_ded

            if line.contract_id.payroll_tax:
                total_tax = (total - (line.contract_id.payroll_tax.ptkp/12))
                if total_tax > 0:
                    tax_final = total_tax * line.contract_id.percent / 100

                    for record in line.line_ids.filtered(lambda x: x.category_id == tax):
                        record.amount = tax_final

            total_net = total - total_ded

            for record in line.line_ids.filtered(lambda x: x.category_id == net):
                record.amount = total_net

            for record in line.line_ids.filtered(lambda x: x.name == 'Pembulatan'):
                record.amount = round(total_net, -2)

        return result