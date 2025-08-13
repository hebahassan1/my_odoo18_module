# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Mrp Report",
    'version': "1.1",
    'category': "Manufacturing/Manufacturing",
    'summary': 'Print Excel Report for Manufacturing Orders & BOMs',
    'author': "Heba AbdelRazek",
    'data': [
        'views/mrp_production_view.xml',
    ],

    'depends': ['base', 'mrp', 'project'],
    'installable': True,
    'auto_install': False,
    'application': False,
}
