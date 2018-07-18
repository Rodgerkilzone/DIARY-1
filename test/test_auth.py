import unittest
import os
import json
from flask import Flask
from app.app import create_app
from models.user import User
import inspect
import sys
currentdir = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


class EntryTestCase(unittest.TestCase):
    """Test Entry content in app"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.user_registration = {
            "FirstName": "John",
            "LastName": "Doe",
            "Email": "John_Doe@example.com",
            "Password": "its26uv3nf"
        }
        self.user_login = {
            "Email": "John_Doe@example.com",
            "Password": "its26uv3nf"
        }

    def test_encode_auth_token(self):
        user = User(
            firstname="test",
            lastname="tester",
            email='test@test.com',
            password='test123')
        user.create()
        auth_token = user.encode_auth_token(user.email)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_user_signup(self):
        """Test user registration"""
        response = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps(self.user_registration),
            content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'Successfully registered.')
        self.assertEqual(response.status_code, 201)

    def test_signup_names_less_than_two_char(self):
        """Test user signups name with less than two characters"""
        response = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "FirstName": "J",
                "LastName": "Do",
                "Email": "John_Doe@example.com",
                "Password": "its26uv3nf"
            }),
            content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["Message"], "Names should be more than 2 ")
        self.assertEqual(response.status_code, 400)

    def test_signup_names_invalid_char(self):
        """Test user signups name with invalid characters"""
        response = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "FirstName": "!!!!!!!!!",
                "LastName": "$$$$$$$$$$$$",
                "Email": "John_Doe@example.com",
                "Password": "its26uv3nf"
            }),
            content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["Message"],
                         "Invalid character in your name(s)")
        self.assertEqual(response.status_code, 400)

    def test_signup_email_less_than_four_char(self):
        """Test user signups email with less than four characters"""
        response = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "FirstName": "John",
                "LastName": "Doe",
                "Email": ".co",
                "Password": "its26uv3nf"
            }),
            content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["Message"],
                         "Email should be more than 4 character ")
        self.assertEqual(response.status_code, 400)

    def test_signup_email_invalid_char(self):
        """Test user signups email with invalid characters"""
        response = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "FirstName": "John",
                "LastName": "Doe",
                "Email": "look!!!!!!!!@invalid.com",
                "Password": "its26uv3nf"
            }),
            content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["Message"], "Invalid character in your email ")
        self.assertEqual(response.status_code, 400)

    def test_signup_password_less_than_six_char(self):
        """Test user signups  with less than six characters"""
        response = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps({
                "FirstName": "John",
                "LastName": "Doe",
                "Email": "John_Doe@example.com",
                "Password": "abc"
            }),
            content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["Message"],
                         "Password should be more than 6 character ")
        self.assertEqual(response.status_code, 400)

    #Login
    def test_api_user_login_successfully(self):
        """Test user signin successfully"""
        self.client.post(
            'api/v1/auth/signup',
            data=json.dumps(self.user_registration),
            content_type="application/json")

        login_result = self.client.post(
            'api/v1/auth/login',
            data=json.dumps(self.user_login),
            content_type="application/json")
        print(login_result)
        results = json.loads(login_result.data)
        print(results)
        self.assertEqual(results['message'], 'Successfully login.')

    def test_api_invalid_email(self):
        """Test for invalid email in signin endpoint"""
        response = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps(self.user_registration),
            content_type="application/json")
        self.assertEqual(response.status_code, 201)
        response = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps({
                "Email": "John@example.com",
                "Password": "its26uv3nf"
            }),
            content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'Failed, Invalid email! Please try again')
        self.assertEqual(response.status_code, 401)

    def test_api_invalid_password(self):
        """Test for invalid password in signin endpoint"""
        response = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps(self.user_registration),
            content_type="application/json")
        self.assertEqual(response.status_code, 201)
        response = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps({
                "Email": "John_Doe@example.com",
                "Password": "fakepassword"
            }),
            content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'Failed, Invalid password! Please try again')
        self.assertEqual(response.status_code, 401)
