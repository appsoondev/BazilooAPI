"""
test for models
"""

from core import models
from django.contrib.auth import get_user_model
from django.test import TestCase


def create_user(email='testuser@example.com', password='Password'):
	"""Create and returns a Dummy user for testing purposes."""
	return get_user_model().objects.create_user(email=email, password=password)


class ModelTests(TestCase):
	"""Test Models."""

	def test_create_user_with_email_successful(self):
		"""
			made for testing test_create_user_with_email_successful
		"""
		email = 'test@example.com'
		password = 'testpass123'
		user = get_user_model().objects.create_user(
			email=email,
			password=password
		)

		self.assertEqual(user.email, email)
		self.assertTrue(user.check_password(password))

	def test_new_user_email_normalized(self):
		"""
		test email is normalized for new users
		"""
		sample_emails = [
			['test1@EXAMPLE.com', 'test1@example.com'],
			['Test2@Example.com', 'Test2@example.com'],
			['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
			['test4@example.COM', 'test4@example.com'],
		]

		for email, expected in sample_emails:
			user = get_user_model().objects.create_user(email=email, password='123')
			self.assertEqual(user.email, expected)

	def test_new_user_without_email_raises_error(self):
		"""Test that creating user without email will raise an error"""

		with self.assertRaises(ValueError):
			get_user_model().objects.create_user('', 'password123')

	def test_create_superuser(self):
		"""Test Creating a superuser"""
		user = get_user_model().objects.create_superuser(
			'test@example.com',
			'password123',
		)
		self.assertTrue(user.is_superuser)
		self.assertTrue(user.is_staff)

	def test_create_lead(self):
		"""Test Creating a Lead is successful"""
		user = create_user()
		lead = models.Lead.objects.create(
			user=user,
			email='leademail@example.com',
			phone='+972541096752',
			fname='John',
			lname='Doe',

		)
		self.assertEqual(str(lead), lead.email)
