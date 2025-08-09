# file: reports/report_pos_type_order.py
from odoo import api, models
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

class ReportPosTypeOrder(models.AbstractModel):
    _name = 'report.pos_type_order.report_pos_type_order'
    _description = 'POS Type Order Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data:
            raise UserError("Please use the wizard to print this report.")
    
        
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        config_ids = data.get("config_ids", [])
        active_pos_types = data.get("active_pos_types", [])

        if end_date < start_date:
           raise ValidationError("End Date must be greater than or equal to Start Date.")


        # Search POS orders
        orders = self.env["pos.order"].search([
            ("date_order", ">=", start_date),
            ("date_order", "<=", end_date),
            ("session_id.config_id", "in", config_ids),
            ("pos_type_order_id", "in", active_pos_types),
        ])

        # Count orders per POS Type
        counts = {}
        for order in orders:
            if order.pos_type_order_id:
                counts[order.pos_type_order_id] = counts.get(order.pos_type_order_id, 0) + 1

        # Prepare table rows
        type_counts = []
        for type_rec in self.env["pos.type.order"].browse(active_pos_types):
            type_counts.append({
                "type_name": type_rec.name,
                "order_count": counts.get(type_rec, 0),
            })

        config_names = ", ".join(self.env["pos.config"].browse(config_ids).mapped("name"))

        return {
            "doc_ids": docids,
            "doc_model": "pos.type.order",
            "start_date": start_date,
            "end_date": end_date,
            "config_names": config_names,
            "type_counts": type_counts,
        }
