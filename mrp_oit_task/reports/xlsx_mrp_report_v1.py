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
            {'bold': True, 'font_color': 'black', 'bg_color': '#D3D3D3', 'font_size': 15}
        )
        moves_header_format = workbook.add_format(
            {'bold': True, 'font_color': 'black', 'bg_color': '#b3b0b0', 'font_size': 15}
        )
        date_format = workbook.add_format(
            {'num_format': 'yyyy-mm-dd', 'align': 'center'})

        sheet = workbook.add_worksheet('التصنيع')
        sheet.right_to_left()
        sheet.set_column(1, 7, 20)  # Sets columns B to H to width 20
        s_headers = ['م', 'تاريخ التصنيع', 'رقم اذن التصنيع', 'محطة التصنيع', 'مهندس الجودة'
            , 'اسم الشركة', 'اسم المشروع', 'المحتوي', 'كمية الخرسانة', 'الوحدة '
                     ]
        mrp_ids = request.env['mrp.production'].browse(literal_eval(mrp_ids))
        # Collect unique product_id records from move_raw_ids
        for col, header in enumerate(s_headers):
            sheet.write(0, col, header, header_format)

        unique_products = set()
        index_products = {}
        for mrp in mrp_ids:
            for move in mrp.move_raw_ids:
                unique_products.add(move.product_id)

        # Add unique_products to s_headers
        # s_headers.extend(list(unique_products))
        for col, header in enumerate(unique_products, 10):
            sheet.write(0, col, header.name, moves_header_format)
            index_products[header.id] = (col, header.name)

        sheet.write(0, 10 + len(unique_products), 'الاجمالي', header_format)

        for row, rec in enumerate(mrp_ids, 1):
            total = 0
            sheet.write(row, 0, row)
            sheet.write_datetime(row, 1, rec.date_start, date_format)
            sheet.write(row, 2, rec.name)
            sheet.write(row, 3, rec.location_dest_id.name)
            sheet.write(row, 4, rec.user_id.name)
            sheet.write(row, 5, rec.company_id.name)
            sheet.write(row, 6, rec.project_id.name if rec.project_id.name else " ")
            sheet.write(row, 7, rec.product_id.display_name)
            sheet.write(row, 8, rec.product_qty)
            sheet.write(row, 9, rec.product_uom_id.name)
            for intial in range(10, 10 + len(unique_products)):
                sheet.write(row, intial, 0)

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
