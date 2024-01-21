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
        'base',
    ],
    'data': [
        'views/hr_job_views.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'qweb': [],
}
