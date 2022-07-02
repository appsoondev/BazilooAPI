"""Views for the user API """

from rest_framework import authentication, generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from .serializers import (AuthTokenSerializer, UserSerializer)


class CreateUserView(generics.CreateAPIView):
	"""Create a new user in the system"""
	serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
	"""Create a new Auth Token for user"""
	serializer_class = AuthTokenSerializer
	renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
	"""Manage the authenticated user"""

	serializer_class = UserSerializer
	authentication_classes = [authentication.TokenAuthentication]
	permission_classes = [permissions.IsAuthenticated]

	# overwrite the get object for getting only the user authenticated
	def get_object(self):
		"""
		It returns the authenticated user
		:return: The authenticated user.
		"""
		"""retrieving and returns the authenticated user"""
		return self.request.user
