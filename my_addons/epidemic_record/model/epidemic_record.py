# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class EpidemicRecord(models.Model):
    _name = "epidemic.record"
    name = fields.Char(str="姓名")
    date = fields.Date(str="确诊日期")
    state = fields.Char(str="省")
    city = fields.Char(str="市")
    county = fields.Char(str="区/县")
    street = fields.Char(str="具体地址")
    ill_type = fields.Char(str="感染方式")
    within_or_abroad = fields.Selection([("within","境内"),("abroad","境外")],str="境内/境外感染")
