from odoo import api, fields, models

class HrSalaryRule(models.Model):

    _inherit = "hr.salary.rule"

    type_allowance = fields.Selection([
        ('meal', 'Meal'),
        ('transportation', 'Tranportation'),
        ('basic', 'Basic')
    ], string='Type Allowance')