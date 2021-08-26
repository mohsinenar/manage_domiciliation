# -*- coding: utf-8 -*-

from odoo import models, fields, api


class dashboard(models.Model):
    _name = 'manage.dashboard'
    _auto = False

    color = fields.Integer(string='Color Index')
    name = fields.Char(string="Name")
