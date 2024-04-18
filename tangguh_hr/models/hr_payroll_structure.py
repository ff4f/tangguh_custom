from odoo import api, fields, models

class HrPayrollStructure(models.Model):

    _inherit = "hr.payroll.structure"

    type = fields.Selection([('contract', 'Contract'),
                             ('daily', 'Daily')
                             ], string="Type", default="contract")