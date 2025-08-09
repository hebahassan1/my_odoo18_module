from odoo import models,fields ,api ,_
from odoo.exceptions import UserError
from collections import defaultdict
import logging

class PosTypeOrderWizard(models.TransientModel):
     _name='pos.type.order.wizard'
     _description = 'Wizard to filter POS Type Order Report by date and point of sale'

     start_date = fields.Datetime(default=fields.Datetime.now,required=True)
     end_date = fields.Datetime(default=fields.Datetime.now,required=True)
     config_ids= fields.Many2one('pos.config',string='Point Of Sale',required=True)


     def action_print_report(self):
        active_ids = self.env.context.get('active_ids', [])
        if not active_ids:
            raise UserError("No records selected!")
        
        return self.env.ref("pos_type_order.action_report_pos_type_order").report_action(self.env["pos.type.order"].browse(active_ids),
           data={
                  "start_date": self.start_date,
                  "end_date": self.end_date,
                  "config_ids": self.config_ids.ids,
                  "active_pos_types": active_ids,
                }
                ) 

        