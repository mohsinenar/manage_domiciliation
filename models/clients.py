# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Client(models.Model):
    _name = 'manage.client'
    _description = 'Clients'
    _rec_name='name'

    name = fields.Char(required=True,string="Nom")
    email = fields.Char(required=False,string="E-mail")
    Cin = fields.Char(required=True,string="C.I.N")
    Phone = fields.Char(required=False,string="Téléphone")
    Adress = fields.Text(required=False,string="Adresse")
    company_ids = fields.One2many('manage.company', 'client_id', string='Sociétés')
    company_count = fields.Integer(compute='_compute_company_count', string='Nombre de sociétés')
    domiciliation_ids = fields.One2many('manage.domiciliation','client_id', string='Domiciliations')
    domiciliation_count = fields.Integer(string='Nombre de domiciliations',compute='_compute_domiciliation_count')
    affiliate_id = fields.Many2one(comodel_name='manage.affiliate', string='Source')
    
    # REFRAL 
    @api.depends('company_ids')
    def _compute_company_count(self):
        for record in self:
            record.company_count = len(record.company_ids)

    @api.depends('domiciliation_ids')
    def _compute_domiciliation_count(self):
        for record in self:
            record.domiciliation_count = len(record.domiciliation_ids)


    def action_open_domiciliations(self):
        return {
            'name': ('Domiciliations'),
            'domain': [('client_id','=',self.id)],
            'res_model': 'manage.domiciliation',
            'view_mode': 'tree,form',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'context':{}
            }

    def action_open_companies(self):
        context={'default_client_id':self.id}
        return {
            'name': ('sociétés'),
            'domain': [('client_id','=',self.id)],
            'res_model': 'manage.company',
            'view_mode': 'tree,form',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'context':context
        }