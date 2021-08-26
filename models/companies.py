# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Company(models.Model):
    _name = 'manage.company'
    _description = 'Companies'

    name = fields.Char(required=True,string="Titre")
    company_rc = fields.Integer(required=True,string="RC")
    company_rc_pdf = fields.Binary(required=True,string='RC (PDF)')
    company_if = fields.Integer(required=True,string="IF")
    num_cert = fields.Integer(required=True,string="Numero C.negatif")
    date_cert = fields.Date(required=False,string="date C.negatif")
    company_ICE = fields.Integer(required=True,string="ICE")
    patente = fields.Integer(required=True,string="Patente")
    numero_affiliation = fields.Integer(required=True,string="numero d'affiliation")
    phone = fields.Char(required=True,string="FIX")
    forme = fields.Selection(string='Forme juridique', selection=[('S.A.R.L', 'SARL'), ('none', 'none'),])
    client_id = fields.Many2one('manage.client', string='Client/Propriétaire',required=True)
    domiciliation_ids = fields.One2many('manage.domiciliation', 'company_id', string='domiciliations')
    date_debut = fields.Date(compute='_compute_date_debut', string='date debut')
    last_domiciliation_id = fields.Many2one("manage.domiciliation",compute='_compute_last_domiciliation_id', string='')
    date_fin = fields.Date(related='last_domiciliation_id.Date_fin', string='date fin')
    status = fields.Selection(string='status',compute="_compute_status",selection=[('en_cours', 'en cours'),('ended','terminé'),('close_to_end','se termine dans 15 jours'),('closed','résilié'),('new','new')],store=True,default='new')
    is_cancled = fields.Boolean(related='last_domiciliation_id.is_cancled',string='résilié')
    rest_days = fields.Integer(related='last_domiciliation_id.rest_days')

    
    # @api.onchange('last_domiciliation_id','last_domiciliation_id.status','domiciliation_ids','domiciliation_ids.status','domiciliation_ids.is_cancled')
    @api.depends('last_domiciliation_id','last_domiciliation_id.status','domiciliation_ids','domiciliation_ids.status','domiciliation_ids.is_cancled')
    def _compute_status(self):
        for rec in self:
            if rec.last_domiciliation_id:
                rec.status = rec.last_domiciliation_id.status
            else:
                rec.status = 'new'


    @api.depends('domiciliation_ids')
    def _compute_last_domiciliation_id(self):
        for rec in self:
            if len(rec.domiciliation_ids)>0:
                rec.last_domiciliation_id = rec.domiciliation_ids[-1].id
            else:
                rec.last_domiciliation_id = False


    @api.depends('domiciliation_ids')
    def _compute_date_debut(self):
        for rec in self:
            if len(rec.domiciliation_ids)>0:
                rec.date_debut = rec.domiciliation_ids[0].Date_debut
            else:
                rec.date_debut = False

    def action_open_domiciliations(self):
        context={'default_company_id':self.id}
        return {
            'name': ('Domiciliations'),
            'domain': [('company_id','=',self.id)],
            'res_model': 'manage.domiciliation',
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
            'context':{},
            'res_id': False,
            'target':'current',
            "views": [[False, "form"]],
            "context":context
            }

    def cancel(self):
        for rec in self:
            rec.last_domiciliation_id.is_cancled = True

    def reactivate(self):
        for rec in self:
            rec.last_domiciliation_id.is_cancled = False


