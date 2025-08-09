{
    'name': 'POS Order Type',
    'version': '1.0',
    'summary': 'Manage types of POS orders',
    'description': 'Module to manage and filter POS orders by type.',
    'category': 'Point of Sale',
    'author': 'Heba Abdel Razek',
    'website': '',
    'license': 'LGPL-3',
    'depends': [
        'point_of_sale',
        'base',
        'web',
    ],
    'data': [
        'data/pos_type_order_data.xml',
        'security/ir.model.access.csv',
        'views/pos_order_views.xml',
        'views/pos_type_order_views.xml',
        'wizard/pos_type_order_wizard.xml',
        'report/pos_type_order_template.xml',
        'report/pos_type_order_report.xml',
       
        

    ],
    
    'assets': {
    'point_of_sale._assets_pos': [
        'pos_type_order/static/src/js/order_type_button.js',
        'pos_type_order/static/src/xml/order_type_template.xml',
    ],
},
    'installable': True,
    'application': True,
    'auto_install': False,
    }