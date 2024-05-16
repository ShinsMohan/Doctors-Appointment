from odoo import models, fields, api

class PatientReportXlsx(models.AbstractModel):
    _name = 'report.doctors_appointment.report_patient_prescription_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, patients):
        for obj in patients:
            bold = workbook.add_format({'bold': True})
            date_format = workbook.add_format({'num_format': 'yyyy-mm-dd hh:mm:ss'})

            for appointment in patients:
                sheet = workbook.add_worksheet(appointment.patient_id.name)

                sheet.merge_range(0, 0, 0, 1, 'Patient Name:', bold)
                sheet.write(0, 2, appointment.patient_id.name)

                sheet.merge_range(1, 0, 1, 1, 'Appointment Date:', bold)
                sheet.write_datetime(1, 2, appointment.appointment_date, date_format)

                sheet.merge_range(2, 0, 2, 1, 'Doctor:', bold)
                sheet.write(2, 2, appointment.doctors_id.name)

                sheet.merge_range(3, 0, 3, 1, 'Appointment Type:', bold)
                sheet.write(3, 2, appointment.appointment_type)

                sheet.merge_range(4, 0, 4, 1, 'Prescription:', bold)
                sheet.write(4, 2, appointment.observation)

                sheet.write(6, 0, 'Medicine', bold)
                sheet.write(6, 1, 'Dosage', bold)    
                row = 7

                for prescription_line in appointment.patient_prescription_line_ids:
                    sheet.write(row, 0, prescription_line.medicine_id.name)
                    sheet.write(row, 1, prescription_line.dosage)
                    row += 1

                # Set column width 
                sheet.set_column(1, 1, 20)
                sheet.set_column(1, 1, 20)