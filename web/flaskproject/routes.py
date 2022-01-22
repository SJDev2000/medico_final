from flaskproject import app, db
from flask import request, session, url_for, make_response
from flask.json import jsonify
from werkzeug.utils import redirect, secure_filename
import hashlib
from datetime import datetime, timedelta
import jwt
from flaskproject.decorator import token_required
from flaskproject.doctorDecorator import doctoken_required
from flaskproject.models import Patient, Doctor, Prescription
from flask_restful import Api, Resource, reqparse
from flask.templating import render_template
import os, uuid


# Home Page route

@app.route('/')
def home():
    return render_template('homePage.html')


@app.route('/about', methods=["POST","GET"])
def about():
    if request.method == "POST":
        return render_template('about.html')
    return render_template('about.html')


# sign up for patient

# @app.route('/signUp', methods=["POST", "GET"])
# def signUp():
#     if request.method == "POST":
#         return render_template('register.html')
#     return render_template('register.html')

# @app.route('/signIn', methods=["POST", "GET"])
# def signIn():
#     if request.method == "POST":
#         return render_template('login.html')
#     return render_template('login.html')

# Patient Dashboard
@app.route('/patientDashboard')
@token_required
def patientDashboard(current_user):
    patient = Patient.query.filter_by(email = current_user).first()
    uniqueStr = str(uuid.uuid1())
    return render_template('patientDashboard.html', patient = patient, prescriptions = patient.prescriptions, uniqueStr = uniqueStr)

# Patient Register

@app.route('/createPatient', methods= ["POST", "GET"])
def register():
    if request.method == "POST":
        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]
        hashedPassword = hashlib.md5(bytes(str(password),encoding='utf-8'))
        hashedPassword = hashedPassword.hexdigest() 

        # register the new patient to the database
        patient = Patient.query.filter_by(email = email).first()
        if patient == None:
            new_user = Patient(fullname = fullname, email = email, password = hashedPassword)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login')) #function name and url_for name should be same
        else:
            return "Patient already registered"
    return render_template("register.html")

# Patient Login

@app.route('/patientLogin', methods=["POST","GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        hashedPassword = hashlib.md5(bytes(str(password),encoding='utf-8'))
        hashedPassword = hashedPassword.hexdigest()
        result = Patient.query.filter_by(email = email).first()
        if result == None or hashedPassword != result.password:
            return "Invalid email or password"
        token = jwt.encode({'user':result.email, 'exp': datetime.utcnow()+timedelta(minutes=65)}, app.config['SECRET_KEY'])
        session["jwt"] = token
        return redirect(url_for('patientDashboard'))
    return render_template("login.html")
    
# Patient Profile

@app.route('/patientProfile', methods= ["POST", "GET"])
@token_required
def profile(current_user):
    if request.method == "POST":
        patient = Patient.query.filter_by(email = current_user).first()
        patient.age = request.json["age"]
        patient.gender = request.json["gender"]
        patient.address = request.json["address"]
        patient.phone = request.json["phone"]
        db.session.commit()
    return jsonify({"update": "success"})

# Doctor Login

@app.route('/doctorLogin', methods = ["POST", "GET"])
def docLogin():
    if request.method == "POST":
        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]
        result = Doctor.query.filter_by(email = email).first()
        if result == None or password != result.password:
            return "Invalid email or password"
        token = jwt.encode({'user':result.email, 'exp': datetime.utcnow()+timedelta(minutes=65)}, app.config['SECRET_KEY'])
        session["docjwt"] = token
        return redirect(url_for('doctorDashboard'))
    return render_template('doctorslogin.html')

# Doctor Profiles

@app.route('/doctorProfiles', methods= ["POST", "GET"])
@token_required
def doctorProfiles(current_user):
    doctors = Doctor.query.all()
    return render_template('doctorProfiles.html',doctors = doctors)

@app.route('/vitalProfiles', methods= ["POST", "GET"])
@token_required
def vitalProfiles(current_user):
    patient = Patient.query.filter_by(email = current_user).first()
    vital = Prescription.query.filter_by(patient_id = patient.id).order_by(Prescription.id.desc()).first()
    return render_template('vitals.html',vital = vital)



@app.route('/prescribe/<patient_id>', methods= ["POST", "GET"])
@doctoken_required
def prescribe(current_user, patient_id):
    if request.method == "POST":
        doctor = Doctor.query.filter_by(email = current_user).first()
        bloodPressure = request.form["bp"]
        heartRate = request.form["hr"]
        glucoseLevel = request.form["gl"]
        bloodCount = request.form["bc"]
        oxygenLevel = request.form["bt"]
        bodyWeight = request.form["bw"]
        diagnosisName = request.form["dname"]
        severity = request.form["severe"]
        medicationitem = request.form["drugName"]
        namedTimeEvent = request.form["timeEvent"]
        doseUnits = request.form["munit"]
        doseVolumne = request.form["dunit"]
        frequency = request.form["frequency"]
        interval = request.form["interval"]
        repetetion = request.form["repetition"]
        additionalInstructions = request.form["description"]
        prescription = Prescription(doctor_id = doctor.id, patient_id = patient_id, bloodPressure = bloodPressure, heartRate = heartRate, glucoseLevel = glucoseLevel, bloodCount = bloodCount, oxygenLevel = oxygenLevel, bodyWeight = bodyWeight, diagnosisName = diagnosisName, severity = severity, medicationitem = medicationitem, namedTimeEvent = namedTimeEvent, doseUnits = doseUnits, doseVolumne = doseVolumne, frequency = frequency, interval = interval, repetetion = repetetion, additionalInstructions = additionalInstructions)
        db.session.add(prescription)
        db.session.commit()
        return redirect(url_for('doctorDashboard'))
    return render_template('prescription.html')


# Doctor Dashboard

@app.route('/doctorDashboard', methods= ["POST", "GET"])
@doctoken_required
def doctorDashboard(current_user):
    patients = Patient.query.all()
    return render_template('doctorDashboard.html', patients = patients)


@app.route('/myPatients', methods= ["POST", "GET"])
@doctoken_required
def myPatients(current_user):
    tempList = []
    prescriptions = Prescription.query.all()
    for prescription in prescriptions:
        if prescription.doctor.email == current_user:
            patient = Patient.query.filter_by(id = prescription.patient_id).first()
            if patient not in tempList:
                tempList.append(patient)
    return render_template('doctorDashboard.html', patients = tempList)

@app.route('/doctorInfo')
@doctoken_required
def doctorInfo(current_user):
    doctor = Doctor.query.filter_by(email = current_user).first()
    return render_template('doctorInfo.html', doctor = doctor)

@app.route('/doctorLogout')
@doctoken_required
def doctorLogout(current_user):
    if session.get('jwt') == False:
        session.pop("docjwt")
        session.clear()
    else:
        session.pop('docjwt')
    return redirect(url_for('docLogin'))

@app.route('/patientLogout')
@token_required
def patientLogout(current_user):
    if session.get('docjwt') == False:     # if doctor is already logged out then pop() and clear()
        session.pop("jwt")
        session.clear()
    else:
        session.pop('jwt')               # if doctor is logged in then only pop()
    return redirect(url_for('login'))


@app.route('/updateProfile', methods=["GET"])
@token_required
def updateProfile(current_user):
    patient = Patient.query.filter_by(email = current_user).first()
    print(patient.email)
    return render_template('patientprof.html', patient = patient)

@app.route('/uploadProfile', methods=["POST", "GET"])
@token_required
def uploadProfile(current_user):
    patient = Patient.query.filter_by(email = current_user).first()
    if request.method == "POST":
        fullname = request.form['fullname']
        age = request.form['age']
        gender = request.form['gender']
        address = request.form['address']
        phone = request.form['phone']
    
        patient.fullname = fullname
        patient.age = age
        patient.gender = gender
        patient.address = address
        patient.phone = phone
        
        db.session.commit()
        return render_template('patientprof.html', patient = patient)
    return render_template('patientprof.html', patient = patient)