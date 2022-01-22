import pytest
from flaskproject import app,db
from flaskproject.models import Patient, Doctor


@pytest.fixture(scope='module')
def test_client():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TESTING"]= True
   


    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client  # this is where the testing happens!



@pytest.fixture(scope='module')
def init_db(test_client):
    db.create_all()
    patient= Patient(fullname="Shreyal",email="shreyal@gmail.com",password="12345678")
    doctor= Doctor(fullname="Steve",email="steve@gmail.com",password="12345678")
    db.session.add(doctor)
    db.session.add(patient)
    db.session.commit()

    yield 

    db.drop_all()


@pytest.fixture(scope='module')
def login_user(test_client):
    test_client.post('/patientLogin', data=dict(
    email="shreyal@gmail.com",password="12345678"
    ),follow_redirects= True)

    yield 

    db.drop_all()

