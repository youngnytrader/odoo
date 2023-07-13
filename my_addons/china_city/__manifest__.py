# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': '城市信息',
    'summary': '''城市信息''',
    'description': '''城市信息''',
    "author": "youngny",
    'version': '1.0',
    'depends': ['base','base_address_extended'],
    'data': [
        "views/res_city_view.xml",
        "views/menu_views.xml",

    ],

    'installable': True,
    "application": True,

}
