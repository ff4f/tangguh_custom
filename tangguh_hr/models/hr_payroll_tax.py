from odoo import api, fields, models

class HrPayrollTax(models.Model):

    _name = "hr.payroll.tax"

    name = fields.Char("Name")
    percent = fields.Float("Percent")

    @api.multi
    def name_get(self):
        result = []
        for line in self:
            name = line.name + ' ' + line.percent
            result.append((line.id, name))
        return result