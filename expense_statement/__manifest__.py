# -*- coding: utf-8 -*-
{
    'name': "expense_statement",

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
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'branch'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/expense_state_wizard.xml',
        'views/account_account_inherited.xml',
        'reports/report.xml',
        'reports/templates.xml'
    ],

}
