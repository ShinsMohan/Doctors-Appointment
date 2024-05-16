# import json
# import io
# import xlsxwriter
from odoo import api, models, fields
# from odoo.tools import date_utils

class PatientAppointment(models.Model):
    _name = "patient.appointment"
    _description = "Patient Records"

    patient_id = fields.Many2one('res.partner', string="Patient")
    doctors_id = fields.Many2one('hr.employee', string="Doctor")
    appointment_date = fields.Datetime(string="Appointment Date")
    appointment_type = fields.Selection([('checkup', 'Checkup'),('treatment', 'Treatment'),('consultation', 'Consultation')],string='Appointment Type')
    observation = fields.Text(string="Observation")
    pharmacy_line_ids = fields.One2many('patient.pharmacy.lines', 'appointment_id', string='Pharmacy Lines')
    patient_prescription_line_ids = fields.One2many('patient.prescription.line','prescription_id',string='Prescription Lines')
    total_amount = fields.Float(string="Total Amount", compute="_compute_total_amount", store=True)

    @api.depends('pharmacy_line_ids.total')
    def _compute_total_amount(self):
        for appointment in self:
            appointment.total_amount = sum(line.total for line in appointment.pharmacy_line_ids)

#

    def patient_report_sheet(self):
        data = {
            'patient_id': self.patient_id,
            'appointment_type': self.appointment_type,
            'appointment_date': self.appointment_date,
            'observation': self.observation,
            'total_amount': self.total_amount,
            'doctors_id': self.doctors_id,
        }
    #     if data:
    #         return{
    #             'type':'ir.action.report',
    #             'data': { 
    #                 'model': 'patient_report_sheet',
    #                 'options': json.dumps(data, default=date_utils.json_default()),
    #                 'output_format': 'xlsx',
    #                 'report_name': 'Patient Report'
    #             },
    #             'report_type':'xlsx'
    #         }
    # def get_xlxs_report(self, data, response):
    #     output = io.BytesIO()
    #     workbook = xlsxwriter.Workbook (output, {'in_memory': True})    
    #     sheet = workbook.add_worksheet()
    #     cell_format = workbook.add_format(
    #         {'font_size': '12px', 'align': 'center'})
    #     head = workbook.add_format(
    #         {'align': 'center', 'bold': True, 'font_size': '20px'})
    #     headings = workbook.add_format(
    #         {'font_size': '11px', 'font_color': '#FFFFFF', 'align': 'center',
    #         'bold': True, 'bg_color': '#000000'})
    #     sheet.merge_range('D2:H3', f" Student Details", head)
    #     sheet.set_column('C:C', 20)
    #     sheet.set_column ('D:D', 20)
    #     sheet.set_column('E:E', 20)
    #     sheet.set_column('F:F', 20)
    #     sheet.set_column('G:G', 20)
    #     print('def')
    #     row = 5
    #     col = 2
    #     sheet.write(row, col, 'patient_id', headings)
    #     sheet.write(row, col + 1, 'appointment_type', headings)
    #     sheet.write(row, col + 2, 'appointment_date', headings)
    #     sheet.write(row, col+ 3, 'observation', headings)
    #     sheet.write(row, col + 4, 'total_amount', headings)
    #     sheet.write(row, col + 5, 'doctors_id', headings)
    #     row += 1
    #     sheet.write(row, col, data['patient_id'], cell_format)
    #     sheet.write(row, col+1, data['appointment_type'], cell_format)
    #     sheet.write(row, col+1, data['appointment_type'], cell_format)
    #     sheet.write(row, col+1, data['appointment_type'], cell_format)
    #     sheet.write(row, col + 2, data['appointment_date'], cell_format)
    #     sheet.write(row, col + 3, data['observation'], cell_format)
    #     sheet.write(row, col + 4, data['total_amount'], cell_format)
    #     sheet.write(row, col+ 5, data['doctors_id'], cell_format)
    #     workbook.close()
    #     output.seek (0)
    #     response.stream.write(output.read())
    #     output.close()

#

class PatientPharmacyLines(models.Model):
    _name = "patient.pharmacy.lines"
    _description = "Patient Pharmacy Lines"

    medicine_id = fields.Many2one('product.product', string="Medicine")
    quantity = fields.Integer(string="Quantity")
    unit_price = fields.Float(string="Unit Price")
    total = fields.Float(string="Total", compute="_compute_total", store=True)
    appointment_id = fields.Many2one('patient.appointment', string="Appointment")
    in_prescription = fields.Boolean(default=False, string='In Prescription' )

    @api.depends('quantity', 'unit_price')
    def _compute_total(self):
        for line in self:
            line.total = line.quantity * line.unit_price


    def addto_prescription(self):
        return {
        
            'name': 'Add Medicine to Prescription',
            'view_mode': 'form',
            'res_model': 'patient.prescription.wizard',          
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context':{
                'default_medicine_id':self.medicine_id.id,
                'default_appointment_id':self.appointment_id.id,
                'default_treatment_id':self.id,

            }
        }
    
    def action_remove_from_prescription(self):
        prescription_lines = self.env['patient.prescription.line'].search([
            ('medicine_id', '=', self.medicine_id.id),
            ('prescription_id', '=', self.appointment_id.id)
        ])
        if prescription_lines:
            prescription_lines.unlink()
            self.in_prescription = False
        return {'type': 'ir.actions.act_window_close'}
    
class PatientPrescriptionLine(models.Model):
    _name = 'patient.prescription.line'
    _description = 'Patient Prescription Line'

    medicine_id = fields.Many2one('product.product', string="Medicine")
    prescription_id = fields.Many2one('patient.appointment', string="Appointment")
    dosage = fields.Char(string="Dosage")