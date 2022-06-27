"""
tests for the user api
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


TEST_EMAIL = 'test@example.com'
TEST_NAME = 'Test Name'
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
	"""helper function for creating a new user"""
	return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
	"""Test the Public Features of the user API"""

	def setUp(self):
		"""
			creating the client
		"""
		self.client = APIClient()

	def test_create_user_success(self):
		"""test creating a user is successful"""

		payload = {
			'email':    TEST_EMAIL,
			'password': 'password123',
			'name':     TEST_NAME
		}

		response = self.client.post(CREATE_USER_URL, payload)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		user = get_user_model().objects.get(email=payload.get('email'))
		self.assertTrue(user.check_password(payload.get('password')))
		self.assertNotIn('password', response.data)

	def test_user_with_email_exist_error(self):
		"""Test error returned if user with email exist"""

		payload = {
			'email':    TEST_EMAIL,
			'password': 'password123',
			'name':     TEST_NAME
		}
		create_user(**payload)
		response = self.client.post(CREATE_USER_URL, payload)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_password_too_short_error(self):
		"""test an error returned if password is too short"""

		payload = {
			'email':    TEST_EMAIL,
			'password': 'pass',
			'name':     TEST_NAME
		}
		response = self.client.post(CREATE_USER_URL, payload)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		user_exists = get_user_model().objects.filter(
			email=payload.get('email')
		).exists()

		self.assertFalse(user_exists)

	def test_create_token_for_user(self):
		"""generates a token for valid credentials"""
		user_details = {
			'email':    TEST_EMAIL,
			'password': 'password123',
			'name':     TEST_NAME
		}
		create_user(**user_details)

		payload = {
			'email':    user_details.get('email'),
			'password': user_details.get('password')
		}

		response = self.client.post(TOKEN_URL, payload)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn('token', response.data)

	def test_create_token_bad_credentials(self):
		"""Test returned error if were given bad credentials"""
		create_user(email='test@example.com', password='goodpass')

		payload = {
			'email':    TEST_EMAIL,
			'password': 'badpass',
		}
		response = self.client.post(TOKEN_URL, payload)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertNotIn('token', response.data)

	def test_creat_token_blank_password(self):
		"""Test posting a blank password returns an error"""
		payload = {
			'email':    'test@exmaple.com',
			'password': '',
		}
		response = self.client.post(TOKEN_URL, payload)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertNotIn('token', response.data)

	def test_retrieve_user_unauthorized(self):
		"""Test Authentication is required for users """
		response = self.client.get(ME_URL)

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
	"""Test API Request that require Authentication."""

	def setUp(self):
		""" setting up Client and user for the tests
		"""
		self.client = APIClient()
		self.user = create_user(
			email='test@exmaple.com',
			password='password123',
			name='Test Name'
		)
		self.client.force_authenticate(self.user)

	def test_retrieve_profile_success(self):
		"""Test retrieving the profile of the logged user"""
		response = self.client.get(ME_URL)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(
			response.data, {
				'name':  self.user.name,
				'email': self.user.email,
			})

	def test_post_me_is_not_allowed(self):
		"""Test post method get rejected for the me endpoint"""
		response = self.client.post(ME_URL, {})
		self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

	def test_update_user_profile(self):
		"""Updating the user for the authenticated user"""

		payload = {
			'name':     'updated_name',
			'password': 'newpassword'
		}
		response = self.client.patch(ME_URL, payload)

		self.user.refresh_from_db()
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(self.user.name, payload.get('name'))
		self.assertTrue(self.user.check_password(payload.get('password')))
