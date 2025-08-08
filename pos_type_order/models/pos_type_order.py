from odoo import models, fields 

class PosTypeOrder(models.Model): 
    _name = 'pos.type.order'
    _description = 'POS Type Order' 

    name = fields.Char(string='Name', required=True) 
    active = fields.Boolean(default=True)
    pos_order_ids = fields.One2many('pos.order', 'pos_type_order_id', string="Orders") 
    pos_order_count = fields.Integer(string='Orders Count', compute='_compute_pos_order_count') 
    
    def _compute_pos_order_count(self): 
         for rec in self: 
             rec.pos_order_count = len(rec.pos_order_ids)
             
