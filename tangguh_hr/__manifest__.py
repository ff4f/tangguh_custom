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
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_payroll_tax_views.xml',
        'views/hr_job_views.xml',
        'views/hr_contract_views.xml',
        'views/hr_attendance_views.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'qweb': [],
}
