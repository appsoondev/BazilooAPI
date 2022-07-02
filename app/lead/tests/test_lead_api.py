"""
Test for Lead API
"""

from core.models import Lead
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from lead.serializers import LeadSerializer
from rest_framework import status
from rest_framework.test import APIClient


# Creating url for the lead list view.
LEAD_URL = reverse('lead:lead-list')


def detail_url(lead_id):
	"""
	It takes a lead_id as an argument, and returns an url that points to the detail page of the lead with that id
	:param lead_id: This is the id of the lead that we want to retrieve
	:return: The url for the lead-detail page
	"""
	return reverse('lead:lead-detail', args=[lead_id])


def create_lead(user, **params):
	"""
	It creates a lead with the given user and parameters

	:param user: The user who will be assigned to the lead
	:return: A lead object is being returned.
	"""

	defaults = {
		'fname': 'John',
		'lname': 'Doe',
		'email': 'leadtest@example.com',
		'phone': '0987654321',
	}

	defaults.update(params)
	lead = Lead.objects.create(user=user, **defaults)
	return lead


def create_user(email='user@example.com', password='Password'):
	"""
	Create and return a new user

	:param email: The email address of the user, defaults to user@example.com (optional)
	:param password: The password for the user, defaults to Password (optional)
	:return: A new user object.
	"""
	return get_user_model().objects.create_user(email, password)


class PublicLeadApiTests(TestCase):
	""" This class tests the public (unauthenticated) lead API. """

	def setUp(self):
		"""It creates a new client that we can use to make requests to the API."""
		self.client = APIClient()

	def test_auth_required(self):
		"""
		We're making a GET request to the LEAD_URL without logging in, and we're expecting a 401 (UNAUTHORIZED) response
		"""
		response = self.client.get(LEAD_URL)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateLeadAPITest(TestCase):
	"""This class tests the private (authenticated users) lead API."""

	def setUp(self):
		"""
		We create a user and a client, and then we force the client to authenticate with the user
		"""
		self.user = create_user()
		self.client = APIClient()
		self.client.force_authenticate(self.user)

	def test_retrieve_leads(self):
		"""
		We create two leads, then we make a GET request to the LEAD_URL endpoint
		"""
		create_lead(user=self.user)
		create_lead(user=self.user)
		response = self.client.get(LEAD_URL)

		leads = Lead.objects.all().order_by('-id')
		serializer = LeadSerializer(leads, many=True)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, serializer.data)

	def test_lead_list_limited_to_user(self):
		"""Test that the lead is limited to its own user"""

		other_user = create_user(email='other@example.com', password='password123')

		create_lead(user=other_user)
		create_lead(user=self.user)

		response = self.client.get(LEAD_URL)
		leads = Lead.objects.filter(user=self.user)
		serializer = LeadSerializer(leads, many=True)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, serializer.data)

	def test_get_lead_detail(self):
		"""
		It tests that the get_lead_detail function returns a 200 status code and the correct data
		"""
		lead = create_lead(user=self.user)
		url = detail_url(lead.id)

		response = self.client.get(url)
		serializer = LeadSerializer(lead)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, serializer.data)

	def test_create_lead(self):
		"""
		creating a new lead with the payload data, and then we're checking that the response status code is 201
		(created), and that the lead was created with the correct data
		"""
		payload = {
			'fname': 'John',
			'lname': 'Doe',
			'email': 'leadtest@example.com',
			'phone': '+972541096752',
		}

		response = self.client.post(LEAD_URL, payload)  # /api/leads/lead/

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

		lead = Lead.objects.get(id=response.data['id'])

		self.assertEqual(lead.user, self.user)

		for k, v in payload.items():
			self.assertEqual(getattr(lead, k), v)

	def test_delete_lead(self):
		"""Test deletion of lead successful"""

		lead = create_lead(user=self.user)
		url = detail_url(lead.id)
		response = self.client.delete(url)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertFalse(Lead.objects.filter(id=lead.id).exists())

	def test_delete_other_user_recipe_error(self):
		"""Test trying to delete another user creates error"""
		new_user = create_user(email='newuser@example.com', password='password123')
		lead = create_lead(user=new_user)

		url = detail_url(lead.id)

		response = self.client.delete(url)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
		self.assertTrue(Lead.objects.filter(id=lead.id).exists())
