"""
Summary: Handles user signup, login, and token verification using Firebase Authentication.
"""
import pyrebase
from firebase_admin import auth as admin_auth

config = {
    "apiKey": "AIzaSyCUuvFDAkI4Uz22GguywoL4KqHOekvrBVc",
    "authDomain": "customer-cloud-project.firebaseapp.com",
    "projectId": "customer-cloud-project",
    "storageBucket": "customer-cloud-project.firebasestorage.app",
    "messagingSenderId": "684650349948",
    "appId": "1:684650349948:web:2f31a22ac565a0c8bb90f9",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(config)
auth_client = firebase.auth()

def signup(email: str, password: str):
    return auth_client.create_user_with_email_and_password(email, password)

def login(email: str, password: str):
    return auth_client.sign_in_with_email_and_password(email, password)

def verify_token(id_token: str):
    return admin_auth.verify_id_token(id_token)
