# -*- coding: utf-8 -*-
{
    'name': "SMC Project(Discount Approval,Sale Discontinue)",

    'summary': """
    Discount 
   """,

    'description': """
        Customize some fields in product template
    """,

    'author': "Tabeer Aslam",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'stock', 'sale', 'account', 'discount_sale_order'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/groups.xml',
        'views/views.xml',
        'data/data.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
