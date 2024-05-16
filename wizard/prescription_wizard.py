from odoo import fields, models

class PatientPrescriptionWizard(models.TransientModel):
    _name = 'patient.prescription.wizard'
    _description = 'Patient Prescription Wizard'

    medicine_id = fields.Many2one('product.product', string="Medicine")
    dosage = fields.Char(string="Dosage")
    appointment_id = fields.Many2one('patient.appointment', string="Appointment")
    treatment_id = fields.Many2one('patient.pharmacy.lines', string="Treatment")

    def action_submit(self):
        if self.appointment_id:
            prescription_line = {
                'medicine_id': self.medicine_id.id,
                'dosage': self.dosage,
                'prescription_id': self.appointment_id.id,
            } 
            prescription_line_record = self.env['patient.prescription.line'].create(prescription_line)
            self.treatment_id.in_prescription = True
        return {'type': 'ir.actions.act_window_close'}