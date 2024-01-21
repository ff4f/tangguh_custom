from odoo import api, fields, models

class HrJob(models.Model):

    _inherit = "hr.job"

    wage = fields.Monetary('Wage', digits=(16, 2), required=True)
    currency_id = fields.Many2one(string="Currency", related='company_id.currency_id', readonly=True)
