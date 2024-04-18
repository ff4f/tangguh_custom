from odoo import api, fields, models

class HrPayrollTax(models.Model):

    _name = "hr.payroll.tax"

    name = fields.Char("Name")
    percent = fields.Float("Percent")
    ptkp = fields.Float("PTKP")
    tax_line = fields.One2many("hr.payroll.tax.line", "payroll_tax_id")

class HrPayrollTaxLine(models.Model):

    _name = "hr.payroll.tax.line"

    payroll_tax_id = fields.Many2one("hr.payroll.tax", "PTKP")
    value_min = fields.Float("Nilai Min")
    value_max = fields.Float("Nilai Max")
    percent = fields.Float("Percent")
