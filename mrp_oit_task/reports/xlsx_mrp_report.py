from ast import literal_eval
from odoo import http
from odoo.http import request
import io, datetime, xlsxwriter


class XlsxMrpReport(http.Controller):

    @http.route('/mrp_production/xlsx_report/<string:mrp_ids>', type='http', auth='user')
    def get_xlsx_report(self, mrp_ids):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        header_format = workbook.add_format(
            {'bold': True, 'font_color': 'black', 'bg_color': '#E0E0E0', 'font_size': 15})
        moves_header_format = workbook.add_format(
            {'bold': True, 'font_color': 'black', 'bg_color': '#b3b0b0', 'font_size': 15})
        date_format = workbook.add_format({'num_format': 'yyyy-mm-dd', 'align': 'center'})

        sheet = workbook.add_worksheet('التصنيع')
        sheet.right_to_left()
        sheet.set_column(1, 7, 20)

        s_headers = [
            'م', 'تاريخ التصنيع', 'رقم اذن التصنيع', 'محطة التصنيع', 'مهندس الجودة',
            'اسم الشركة', 'اسم المشروع', 'المحتوي', 'كمية الخرسانة', 'الوحدة '
        ]

        mrp_ids = request.env['mrp.production'].browse(literal_eval(mrp_ids))

        # Collect unique products
        unique_products = {move.product_id for mrp in mrp_ids for move in mrp.move_raw_ids}
        index_products = {prod.id: (col, prod.name) for col, prod in enumerate(unique_products, 10)}

        # Write headers
        self.write_row(sheet, 0, s_headers, header_format)
        for col, prod in enumerate(unique_products, 10):
            sheet.write(0, col, prod.name, moves_header_format)
        sheet.write(0, 10 + len(unique_products), 'الاجمالي', header_format)

        # Write data rows
        for row, rec in enumerate(mrp_ids, 1):
            static_values = [
                row,
                rec.date_start,
                rec.name,
                rec.location_dest_id.name,
                rec.user_id.name,
                rec.company_id.name,
                rec.project_id.name or " ",
                rec.product_id.display_name,
                rec.product_qty,
                rec.product_uom_id.name
            ]
            self.write_row(sheet, row, static_values, None, date_format=date_format)
            # Fill product columns with 0
            for col in range(10, 10 + len(unique_products)):
                sheet.write(row, col, 0)
            total = 0
            for move in rec.move_raw_ids:
                if move.product_id.id in index_products:
                    col, _ = index_products[move.product_id.id]
                    sheet.write(row, col, move.product_uom_qty)
                    total += move.product_uom_qty
            sheet.write(row, 10 + len(unique_products), total, header_format)

        workbook.close()
        output.seek(0)
        file_name = 'mrp_production_report.xlsx'
        return request.make_response(
            output.getvalue(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', f'attachment; filename={file_name}'),
            ]
        )

    @staticmethod
    def write_row(sheet, row, values, cell_format=None, date_format=None):
        for col, value in enumerate(values):
            if isinstance(value, datetime.date) and date_format:
                sheet.write_datetime(row, col, value, date_format)
            else:
                sheet.write(row, col, value, cell_format)
