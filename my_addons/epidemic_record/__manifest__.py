# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': '疫情记录',
    'summary': '''疫情记录''',
    'description': '''疫情记录''',
    "author": "youngny",
    'version': '1.0',
    'depends': [],

    'data': [
        "security/ir.model.access.csv",
        "security/epidemic_record_security.xml",
        "views/epidemic_record_view.xml",
        "views/sheet_view.xml",
    ],

    'installable': True,
    "application": True,
    'assets': {
                'web.assets_backend': [
                    # 'static/src/css/yiqstyle.scss',
                    'epidemic_record/static/src/scss/yiqstyle.scss'
                ],
            },
}
