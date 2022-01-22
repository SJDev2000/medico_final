import pytest

# Patient register and login unit tests

def test_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
  
def test_valid_patient_login(test_client,init_db):
    response = test_client.post('/patientLogin', data=dict(
    email="shreyal@gmail.com",password="12345678"
    ),follow_redirects= True)
    assert response.status_code == 200    

def test_invalid_patient_login(test_client,init_db):
    response = test_client.post('/patientLogin', data=dict(
    email="prishe@gmail.com",password="12"
    ),follow_redirects= True)
    assert response.status_code == 200 
    assert b'Invalid email or password' in response.data  

def test_patient_signup(test_client):
    response = test_client.post('/createPatient', data=dict(
        fullname="Priyanshi",email="priyanshi@gmail.com",password="priyanshi"
    ),follow_redirects= True)
    assert b'Patient already registered' not in response.data

def test_duplicate_patient_signup(test_client, init_db):
    response = test_client.post('/createPatient', data = dict(fullname="Shreyal",email="shreyal@gmail.com",password="12345678"), follow_redirects= True)
    assert b'Patient already registered' in response.data


# Doctor login unit tests

def test_valid_doctor_login(test_client,init_db):
    response = test_client.post('/doctorLogin', data=dict(
    fullname="Steve", email="steve@gmail.com",password="12345678"
    ),follow_redirects= True)
    assert b'Invalid email or password' not in response.data  

def test_invalid_doctor_login(test_client,init_db):
    response = test_client.post('/doctorLogin', data=dict(
    fullname="Steve", email="steve@gmail.com",password="87654321"
    ),follow_redirects= True)
    assert b'Invalid email or password' in response.data  