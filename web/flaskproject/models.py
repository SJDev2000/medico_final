from asyncio import events
from calendar import day_abbr
from ctypes.wintypes import MSG
from sqlalchemy.orm import backref
from flaskproject import db

class Patient(db.Model):
    __tablename__="patient"
    id = db.Column(db.Integer, primary_key=True)
    prescriptions = db.relationship('Prescription',backref='patient',lazy="dynamic")
    fullname = db.Column(db.String(120), unique = False)
    email = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(120), unique = False)
    age = db.Column(db.Integer, nullable = True)
    gender = db.Column(db.String(20), nullable = True)
    address = db.Column(db.String(120), nullable = True)
    phone = db.Column(db.String(15), nullable = True)

    # Deprecated attributes
    image = db.Column(db.Text, nullable = True)
    filename = db.Column(db.Text, nullable = True)
    mimetype = db.Column(db.Text, nullable = True)
    
    def __repr__(self):
        return f"Patient('{self.fullname}', '{self.email}')" 

class Doctor(db.Model):
    __tablename__="doctor"
    id = db.Column(db.Integer, primary_key=True)
    prescriptions = db.relationship('Prescription',backref='doctor',lazy="dynamic")
    fullname = db.Column(db.String(120), unique = False)
    email = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(120), unique = False)
    image = db.Column(db.String(1000), nullable = True)
    desc = db.Column(db.String(200), nullable = True)
    
    def __repr__(self):
        return f"Doctor('{self.fullname}', '{self.email}')" 

class Prescription(db.Model):
    __tablename__="prescription"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.ForeignKey("patient.id"))
    doctor_id = db.Column(db.ForeignKey("doctor.id"))

    #vitals attributes
    bloodPressure = db.Column(db.String(50), nullable = True)
    heartRate = db.Column(db.Integer, nullable = True)
    glucoseLevel = db.Column(db.String(50), nullable = True)
    bloodCount = db.Column(db.Integer, nullable = True)
    oxygenLevel = db.Column(db.Integer, nullable = True)
    bodyWeight =  db.Column(db.Integer, nullable = True)

    #prescription attributes
    medicationitem = db.Column(db.String(50), nullable = True) # Name of the medicine
    diagnosisName = db.Column(db.String(100), nullable = True) # Name of the disease
    namedTimeEvent = db.Column(db.String(150), nullable = True) # before or after meal dropdown
    doseUnits = db.Column(db.Integer, nullable = True) # number of mg or ml's
    doseVolumne = db.Column(db.String(5), nullable = True) # mg or ml
    frequency =  db.Column(db.Integer, nullable = True) # specify in /day
    interval = db.Column(db.Integer, nullable = True) # specify in hours
    additionalInstructions = db.Column(db.String(500), nullable = True) # Textarea
    severity = db.Column(db.String(20), nullable = True) # moderate, normal, serious
    repetetion = db.Column(db.Integer, nullable = True) #how many days to repeat


    
    def __repr__(self):
        return f"Prescription('{self.id}', '{self.email}')" 

