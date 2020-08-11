# -*- coding: utf-8 -*-
# This file is part of OpenERP. The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.
{
    'name' : 'MO Inventory Adjustment',
    'version': '12.0',
    'author': 'cube48 AG',
    'category': 'Custom',
    'website': 'http://www.cube48.de',
    'description': '''
This module create Inventory Adjustment from MO it self. ''',
    'depends': [
        'base', 'mrp', 'stock'
    ],
    'data': [
        'view/mrp_view.xml',
    ],
    'installable': True,
    'application': False,
}
