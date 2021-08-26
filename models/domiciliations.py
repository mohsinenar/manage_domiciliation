# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Domiciliation(models.Model):
    _name = 'manage.domiciliation'
    _description = 'Domiciliations'
    _rec_name = "referance"


    referance = fields.Char(string='Réference', required=True, copy=False, readonly=True,index=True, default="New")
    Date_debut = fields.Date(string="Date début",required=True,default=fields.Datetime.now())
    Date_fin = fields.Date(string="Date Fin",compute='_compute_Date_fin')
    adresse = fields.Text(string='Adresse',required=True)
    duree = fields.Integer(string='Durée',default=6,required=True)
    prix = fields.Monetary(string="Prix/mois",currency_field="currency_id")
    prix_total = fields.Monetary(string="Total",compute='_compute_prix_total',currency_field="currency_id")
    company_id = fields.Many2one('manage.company', string='société',required=True,readonly=True)
    client_id  = fields.Many2one(store=True,related='company_id.client_id',readonly=True)
    currency_id = fields.Many2one('res.currency',required=True, string='Currency',default=lambda self: self.env.user.company_id.currency_id,track_visibility="always")
    rest_days = fields.Integer(compute='_compute_rest_days', string='nombre des jours pour fin:',default=0)
    status = fields.Selection(compute='_compute_status',selection=[('en_cours', 'en cours'),('ended','terminé'),('close_to_end','se termine dans 15 jours'),('closed','résilié')])
    is_cancled = fields.Boolean(default=False,string='résilié')
    cancled_in = fields.Date(string='résilié le',readonly=True)
    paiment_ids = fields.One2many(comodel_name='manage.paiment', inverse_name='domiciliation_id', string='paiments')
    
    
    
    @api.depends('rest_days')
    def _compute_status(self):
        for rec in self:
            if rec.rest_days >15:
                rec.status="en_cours"
            elif rec.rest_days<15 :
                rec.status="close_to_end"
            if rec.rest_days==0 :
                rec.status="ended"
            if rec.is_cancled:
                rec.status="closed"
                
            


    @api.depends('Date_debut','Date_fin')
    def _compute_rest_days(self):
        for rec in self:
            rest_days = (rec.Date_fin - fields.Date.today()).days
            if rest_days > 0 :
                rec.rest_days = rest_days
            else:
                rec.rest_days = 0
    
   
    @api.depends('Date_debut','duree')
    def _compute_Date_fin(self):
        for rec in self:
            if rec.Date_debut:
                rec.Date_fin =  rec.Date_debut+relativedelta(months =rec.duree )
            else:
                rec.Date_fin = False
    
    @api.depends('prix_total')
    def _compute_prix_total(self):
        for rec in self:
            rec.prix_total = rec.duree*rec.prix
    
    def cancel(self):
        for rec in self:
            rec.is_cancled = True

    @api.onchange('is_cancled')
    def _onchange_is_cancled(self):
        for rec in self:
            if rec.is_cancled:
                rec.cancled_in=datetime.today()
            else:
                rec.cancled_in=False

    @api.model
    def create(self, vals):
        if vals.get('referance','New') =='New':
            vals['referance'] = self.env['ir.sequence'].next_by_code('test_seq')
        res = super(Domiciliation, self).create(vals)
        return res