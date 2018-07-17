import unittest
import os
import json
from flask import Flask
from app.app import create_app
from models.user import User


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

    def test_decode_auth_token(self):
        user = User(
            firstname="test",
            lastname="tester",
            email='test@test.com',
            password='test123')
        user.create()
        auth_token = user.encode_auth_token(user.email)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token == 'test@test.com'))

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
        """Test user signups name with less than two characters"""
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

    def test_api_user_login_successfully(self):
        """Test user signin successfully"""
        response = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps(self.user_registration),
            content_type="application/json")
        self.assertEqual(response.status_code, 201)
        response = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps(self.user_login),
            content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'Successfully login.')
        self.assertEqual(response.status_code, 201)

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
