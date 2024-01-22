from odoo import api, fields, models

class HrContract(models.Model):

    _inherit = "hr.contract"

    meal_allowance = fields.Monetary('Meal Allowance')
    transportation_allowance = fields.Monetary('Transportation Allowance')

    #BPJS
    bpjs_kesehatan_emp = fields.Monetary('BPJS Kesehatan Karyawan', help="BPJS Kesehatan dibayar karyawan")
    bpjs_kesehatan_emp_percent = fields.Float('BPJS Kesehatan Karyawan (%)', help="BPJS Kesehatan dibayar karyawan")
    bpjs_kesehatan_com = fields.Monetary('BPJS Kesehatan', help="BPJS Kesehatan dibayar perusahaan")
    bpjs_kesehatan_com_percent = fields.Float('BPJS Kesehatan (%)', help="BPJS Kesehatan dibayar perusahaan")

    bpjs_ketenagakerjaan_emp = fields.Monetary('BPJS Ketenagakerjaan Karyawan', help="BPJS Ketenagakerjaan dibayar karyawan")
    bpjs_ketenagakerjaan_emp_percent = fields.Float('BPJS Ketenagakerjaan Karyawan (%)', help="BPJS Ketenagakerjaan dibayar karyawan")
    bpjs_ketenagakerjaan_com = fields.Monetary('BPJS Ketenagakerjaan', help="BPJS Ketenagakerjaan dibayar perusahaan")
    bpjs_ketenagakerjaan_com_percent = fields.Float('BPJS Ketenagakerjaan (%)', help="BPJS Ketenagakerjaan dibayar perusahaan")


    @api.onchange('job_id')
    def onchange_job_id(self):
        if self.job_id:
            self.wage = self.job_id.wage

    @api.onchange('bpjs_kesehatan_emp_percent', 'wage')
    def onchange_bpjs_kesehatan_emp_percent(self):
        if self.bpjs_kesehatan_emp_percent or self.wage:
            self.bpjs_kesehatan_emp = self.bpjs_kesehatan_emp_percent * self.wage / 100

    @api.onchange('bpjs_kesehatan_com_percent', 'wage')
    def onchange_bpjs_kesehatan_com_percent(self):
        if self.bpjs_kesehatan_com_percent or self.wage:
            self.bpjs_kesehatan_com = self.bpjs_kesehatan_com_percent * self.wage / 100

    @api.onchange('bpjs_ketenagakerjaan_emp_percent', 'wage')
    def onchange_bpjs_ketenagakerjaan_emp_percent(self):
        if self.bpjs_ketenagakerjaan_emp_percent or self.wage:
            self.bpjs_ketenagakerjaan_emp = self.bpjs_ketenagakerjaan_emp_percent * self.wage / 100

    @api.onchange('bpjs_ketenagakerjaan_com_percent', 'wage')
    def onchange_bpjs_ketenagakerjaan_com_percent(self):
        if self.bpjs_ketenagakerjaan_com_percent or self.wage:
            self.bpjs_ketenagakerjaan_com = self.bpjs_ketenagakerjaan_com_percent * self.wage / 100

