from odoo import api, fields, models
from datetime import datetime, timedelta

class HrAttendance(models.Model):

    _inherit = "hr.attendance"

    def calculate_overtime(self):
        overtime = self.calculate_total_working_hour()
        if overtime > 8:
            return overtime - 8
        else:
            return 0

    def calculate_overtime_weekend(self):
        overtime = self.calculate_total_working_hour()
        return overtime

    def calculate_total_working_hour(self):
        check_in = self.check_in.hour + 7
        check_out = self.check_out.hour + 7
        working_hour = 0
        while check_in < check_out:
            if check_in == 12 or check_in == 17:
                pass
            else:
                working_hour += 1
            check_in += 1
        return working_hour


    @api.depends(
        "check_in",
        "check_out",
        "type"
    )
    def _compute_overtime(self):
        for line in self:
            one_five, two, three, four, overtime = 0, 0, 0, 0, 0
            if line.type == 'weekday':
                overtime = line.calculate_overtime()
                if overtime:
                    line.overtime_working_hour = overtime
                    one_five = 1
                    two = overtime - one_five

                    line.one_five = one_five
                    line.two = two
                    line.three = three
                    line.four = four
            else:
                overtime = line.calculate_overtime_weekend()
                line.overtime_working_hour = overtime
                line.one_five = one_five
                two = overtime if overtime <= 7 else 7
                if overtime >= 7:
                    three = 1
                    four = overtime - three - two
                line.two = two
                line.three = three
                line.four = four

    @api.depends('check_in')
    def _compute_type(self):
        for line in self:
            if line.check_in.strftime("%A") == 'Saturday' or line.check_in.strftime("%A") == 'Sunday':
                type = 'weekend'
            else:
                type = 'weekday'
            line.type = type

    @api.depends(
        "check_in",
        "check_out",
        "type"
    )
    def _compute_total_working_hour(self):
        for line in self:
            line.total_working_hour = line.calculate_total_working_hour()



    job_id = fields.Many2one("hr.job", string="Job Position",
                             related="employee_id.job_id")
    planned_in = fields.Datetime("Planned In")
    planned_out = fields.Datetime("Planned Out")
    resource_calendar_id = fields.Many2one(
        'resource.calendar', 'Working Schedule',
        related="employee_id.resource_calendar_id")
    total_working_hour = fields.Float("Total Working Hour", compute='_compute_total_working_hour')
    normally_working_hour = fields.Float("Normally Working Hour", related='resource_calendar_id.hours_per_day')
    overtime_working_hour = fields.Float("Overtime Hour", compute='_compute_overtime')
    type = fields.Selection([
        ('weekend', 'Weekend'),
        ('weekday', 'Weekday')
    ], string="Type", compute='_compute_type')
    one_five = fields.Float(string="1.5", compute='_compute_overtime')
    two = fields.Float(string="2", compute='_compute_overtime')
    three = fields.Float(string="3", compute='_compute_overtime')
    four = fields.Float(string="4", compute='_compute_overtime')