# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from lxml import etree

from odoo import models, fields, api
from odoo.addons.base.models.ir_ui_view import transfer_modifiers_to_node, transfer_node_to_modifiers
from odoo.exceptions import ValidationError
# from odoo.osv.orm import setup_modifiers
import json

from odoo.http import request


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
    epidemic_line2 = fields.One2many('epidemic.line2', 'epidemic_id', string='疫情id行')
    business_date = fields.Date(string="确诊日期", default=fields.Date.today)
    creat_time = fields.Datetime(string="确诊日期", default=fields.Datetime.now)
    # odoo预留字段
    active = fields.Boolean(default=True)
    situation = fields.Char(string="状态", default="新建")

    @api.model
    def create(self, vals_list):
        res = super(EpidemicRecord, self).create(vals_list)
        return res

    def write(self, values):
        ctx = dict(self._context or {})
        if self.situation == 'processing':
            raise ValidationError(u'审批中单据不能修改！')
        if self.situation == '审核':
            raise ValidationError(u'审批完成单据不能修改！')
        return super(EpidemicRecord, self.with_context(ctx)).write(values)
# 删除按钮触发函数
#     @api.multi()
    def unlink(self):
        ctx = dict(self._context or {})
        print(ctx)
        for obj in self:
            if obj.situation == '审核':
                raise ValidationError(u'审批完成单据不能修改！')
            if obj.situation != '审核':
                super(EpidemicRecord, self).unlink()

    @api.onchange("state", "city", "name")
    def onchange_note(self):
        self.note = "{}省{}市,隔离人员姓名{}".format(self.state, self.city, self.name)
        print(self)

    def inspection(self):

        self.situation = "审核"

    def search_btn(self):
        domain = [("situation", "=", "审核")]
        objs = self.search(domain)
        print(objs)
        users_objs = self.env["res.users"].sudo().browse([2, 2])
        print("users_objs:", users_objs)

        res = super(EpidemicRecord, self).get_view(view_id=None, view_type='form')
        print(res['arch'])

    def create_or_whrite(self):
        # res = self.env["res.users"].create({
        #     "name":"测试账户",
        #     "email":"ceshizhanghu@1.com",
        #     "login":"ceshizhanghu@1.com"
        # })
        user_env = self.env["res.users"]
        user_obj = user_env.search([("name", "=", "测试账户")])
        res = user_obj.write({
            "login": "ceshizhanghu@163.com"
        })

    @api.model
    def get_view(self,view_id=None, view_type='form', **options):

        res = super(EpidemicRecord, self).get_view(view_id=view_id, view_type=view_type, **options)

        if view_type == 'form' :
            doc = etree.XML(res['arch'])
            # print(doc.attrib)
            for node in doc.xpath("//*[name(.)!='tree']/field"):
                # node.set('modifiers', {&quot;readonly&quot;:true})
                # node.xpath("//form")
                modifiers = node.attrib.get('modifiers','{}')
                print(node.attrib)
                if modifiers:
                    modifiers = json.loads(modifiers)
                    # print(type(modifiers))
                    # modifiers = {"readonly": True}
                    if modifiers.get("readonly",'')=='':
                        modifiers["readonly"] = "[('situation','=','审核')]"
                        # modifiers["readonly"]=True
                        node.set('modifiers', json.dumps(modifiers))

            res['arch'] = etree.tostring(doc, encoding='unicode')
                # print(modifiers)
                # transfer_modifiers_to_node(modifiers,node)
                # print(node.attrib["modifiers"]['readonly']=true)
                # transfer_node_to_modifiers(attr,attr)

                # simplify_modifiers(modifiers)
                # transfer_modifiers_to_node(node, res['field']['name'])

        # print(res['arch'])

        # print(res['arch'])
        return res




class EpidemicLine(models.Model):
    #
    _name = "epidemic.line"
    name = fields.Char(string="姓名")
    date = fields.Date(string="接触日期")
    location = fields.Char(string="接触地点")
    within_or_abroad = fields.Selection([("within", "境内"), ("abroad", "境外")], default="within", string="境内/境外感染")
    epidemic_id = fields.Many2one('epidemic.record', string="疫情id")
    situation=fields.Char()


class EpidemicLine2(models.Model):
    #
    _name = "epidemic.line2"
    name = fields.Char(string="姓名2")
    date = fields.Date(string="接触日期2")
    location = fields.Char(string="接触地点2")
    within_or_abroad = fields.Selection([("within", "境内"), ("abroad", "境外")], default="within", string="境内/境外感染2")
    epidemic_id = fields.Many2one('epidemic.record', string="疫情id2")
