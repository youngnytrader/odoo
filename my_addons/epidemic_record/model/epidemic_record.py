# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class EpidemicRecord(models.Model):
    _name = "epidemic.record"
    name = fields.Char(string="姓名")
    date = fields.Date(string="确诊日期")
    state = fields.Char(string="省")
    city = fields.Char(string="市")
    county = fields.Char(string="区/县")
    street = fields.Char(string="具体地址")
    ill_type = fields.Char(string="感染方式")
    within_or_abroad = fields.Selection([("within", "境内"), ("abroad", "境外")], default="within", string="境内/境外感染")
    is_ill = fields.Boolean(string="是否确诊")
    begin_isolation_date = fields.Date(string="起始隔离日期")
    isolation_mode = fields.Selection([("home", "居家隔离"), ("focus", "集中隔离")], string="隔离方式")
    create_user_id = fields.Many2one("res.users", string="填报人", default=lambda self: self.env.uid)
    note = fields.Text(string="说明")
    epidemic_line = fields.One2many('epidemic.line', 'epidemic_id', string='疫情id行')
    business_date = fields.Date(string="确诊日期", default=fields.Date.today)
    creat_time = fields.Datetime(string="确诊日期",default=fields.Datetime.now)

    @api.onchange("state", "city", "name")
    def onchange_note(self):
        self.note = "{}省{}市,隔离人员姓名{}".format(self.state, self.city, self.name)


class EpidemicLine(models.Model):
    #
    _name = "epidemic.line"
    name = fields.Char(string="姓名")
    date = fields.Date(string="接触日期")
    location = fields.Char(string="接触地点")
    within_or_abroad = fields.Selection([("within", "境内"), ("abroad", "境外")], default="within", string="境内/境外感染")
    epidemic_id = fields.Many2one('epidemic.record', string="疫情id")
