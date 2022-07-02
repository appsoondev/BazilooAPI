"""Serializers for the lead API"""
from core.models import (Lead, )
from rest_framework import serializers


class LeadSerializer(serializers.ModelSerializer):
	"""This class is a serializer for the Lead model."""

	class Meta:
		"""
		telling the serializer that it should be using the Lead model,
		We're also telling it that all fields should be read-only.
        This is because we don't want to allow users to update the data via the API.
        We'll be using the API to create new leads, but not to update them.
        """
		model = Lead
		fields = ['id', 'fname', 'lname', 'email', 'phone']
		read_only_fields = ('__all__',)
