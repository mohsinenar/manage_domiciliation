# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Paiment(models.Model):
    _name = 'manage.paiment'
    _description = 'paiments'

    date_paiment= fields.Date(required=True,string="Date")
    method = fields.Char(required=False,string="Method")
    Montant = fields.Monetary(required=True,string="Montant",currency_field="currency_id")
    currency_id = fields.Many2one('res.currency',required=True, string='Currency',default=lambda self: self.env.user.company_id.currency_id,track_visibility="always")
    domiciliation_id = fields.Many2one('manage.domiciliation', string='domiciliation')