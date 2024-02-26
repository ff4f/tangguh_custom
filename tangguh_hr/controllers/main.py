from odoo import http
from odoo.http import content_disposition, request
import io
import xlsxwriter
import datetime



class SaleExcelReportController(http.Controller):
    @http.route([
        '/payslip/excel_payslip_report/<model("hr.payslip.run"):wizard>',
    ], type='http', auth="user", csrf=False)
    def get_payslip_excel_report(self, wizard=None, **args):
        # the wizard parameter is the primary key that odoo sent
        # with the get_excel_report method in the ng.sale.wizard model
        # contains salesperson, start date, and end date

        # create a response with a header in the form of an excel file
        # so the browser will immediately download it
        # The Content-Disposition header is the file name fill as needed

        response = request.make_response(
                    None,
                    headers=[
                        ('Content-Type', 'application/vnd.ms-excel'),
                        ('Content-Disposition', content_disposition('Inventory Header Report in Excel Format' + '.xlsx'))
                    ]
                )

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})

        header_style = workbook.add_format(
            {'font_name': 'Times', 'bold': True, 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'center'})
        text_style = workbook.add_format(
            {'font_name': 'Times', 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'right'})
        text_desc_style = workbook.add_format(
            {'font_name': 'Times', 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'left'})

        for user in wizard:
            # create worksheet/tab per salesperson
            sheet = workbook.add_worksheet('Slip Gaji')
            # set the orientation to landscape
            # sheet.set_landscape()
            # set up the paper size, 9 means A4
            sheet.set_paper(9)
            # set up the margin in inch
            sheet.set_margins(0.5, 0.5, 0.5, 0.5)

            summary_row = 4
