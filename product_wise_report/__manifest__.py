# -*- coding: utf-8 -*-
{
    'name': "product_wise_report",

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
    'category': 'Productivity',
    'version': '0.1',
    'sequence': -100,
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/product_wizard_view.xml',
        'reports/report.xml',
        'reports/product_report_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}
