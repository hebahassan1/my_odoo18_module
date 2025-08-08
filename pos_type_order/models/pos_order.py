from odoo import models,fields,api

class PosOrder(models.Model):
    _inherit = 'pos.order'

    pos_type_order_id = fields.Many2one('pos.type.order',                        
              string='Order Type', help='Type of the order for categorization')
    
  