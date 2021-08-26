# -*- coding: utf-8 -*-

from odoo import models, fields, api


class affiliate(models.Model):
    _name = 'manage.affiliate'
    _description = 'affiliates'
    _rec_name='name'

    name = fields.Char(required=True,string="Nom")
    email = fields.Char(required=False,string="e-mail")
    Phone = fields.Char(required=False,string="Telephone")
    client_ids = fields.One2many('manage.client', 'affiliate_id', string='sociétés')
