{
    "name": "Doctor's Appointment",
    "author": 'Shins',
    'license': 'LGPL-3',
    "depends": ['base','hr','stock','report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/patient_wiz.xml',
        "report/patient_prescription_template.xml",
        "data/header.xml",
        "report/patient_prescription_view.xml",
        'views/menu.xml',
        'views/patients_appoi.xml',
    ]
}