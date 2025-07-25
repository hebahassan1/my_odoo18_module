from odoo import models, fields


class MrpProduction(models.Model):
    """ Manufacturing Orders """
    _inherit = 'mrp.production'

    def print_oit_production_xlsx(self):
        return {
            'type': 'ir.actions.act_url',
            'url': f'/mrp_production/xlsx_report/{self.env.context.get("active_ids")}',
            'target': 'new',
        }
