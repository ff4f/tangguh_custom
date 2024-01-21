from odoo import api, fields, models

class HrContract(models.Model):

    _inherit = "hr.contract"

    @api.onchange('job_id')
    def onchange_job_id(self):
        if self.job_id:
            self.wage = self.job_id.wage
