# -*- coding: utf-8 -*-
{
    'name': "branch_report",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '6.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'branch','sale_enterprise','sale'],

    # always loaded
    'data': [
        #'reports/branch_report_template.xml',
#         'reports/smc_branch_report.xml',------current
        'reports/daily_cash_report.xml',
        'wizard/branch_report.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'reports/branch_report.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
