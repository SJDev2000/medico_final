import pytest
from flaskproject.models import Patient, Doctor

def test_patient_model(test_client, init_db):
    patient = Patient.query.filter_by(email = "shreyal@gmail.com").first()
    assert patient.fullname == 'Shreyal'

def test_doctor_model(test_client, init_db):
    doctor = Doctor.query.filter_by(email = "steve@gmail.com").first()
    assert doctor.fullname == 'Steve'