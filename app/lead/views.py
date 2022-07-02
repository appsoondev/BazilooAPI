"""Views for the lead API"""

from core.models import (Lead)
from lead import serializers
from rest_framework import (mixins, viewsets)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class LeadViewSet(
	mixins.CreateModelMixin,
	mixins.ListModelMixin,
	mixins.DestroyModelMixin,
	mixins.RetrieveModelMixin,
	viewsets.GenericViewSet,
):
	"""A ViewSet for managing the lead API"""
	serializer_class = serializers.LeadSerializer
	queryset = Lead.objects.all()
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		"""retrieving leads for the authenticated user"""
		return self.queryset.filter(user=self.request.user).order_by('-id')

	def perform_create(self, serializer):
		"""Create New Lead"""
		serializer.save(user=self.request.user)
