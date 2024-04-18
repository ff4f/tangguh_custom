# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Tangguh Employees',
    'version': '1.1',
    'category': 'Human Resources',
    'sequence': 75,
    'summary': 'Centralize employee information',
    'description': "",
    'depends': [
        'hr',
        'hr_contract',
        'hr_attendance',
        'hr_payroll',
        'ohrms_salary_advance',
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/tangguh_hr_data.xml',
        # 'wizards/wizard_report_payslip_views.xml',
        'views/hr_payroll_structure_views.xml',
        'views/hr_payroll_tax_views.xml',
        'views/hr_salary_rule_views.xml',
        'views/hr_job_views.xml',
        'views/hr_contract_views.xml',
        'views/hr_attendance_views.xml',
        'views/hr_payslip_run_views.xml',
        'views/salary_advance_views.xml',
        'report/report_payslip_templates.xml',
        'report/hr_payslip_reports.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'qweb': [],
}
