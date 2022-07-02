"""
Serializers for the user API view
"""
from django.contrib.auth import (authenticate, get_user_model)
from django.utils.translation import gettext as _
from rest_framework import serializers



class UserSerializer(serializers.ModelSerializer):
	"""
	The UserSerializer class has the email, password, and name fields.
    The password field is write only and has a minimum length of 5.
	"""

	class Meta:
		"""Metadata for the user serializer"""
		model = get_user_model()
		fields = ['email', 'password', 'name']
		extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

	def create(self, validated_data):
		"""Create and Return a user with encrypted password"""
		return get_user_model().objects.create_user(**validated_data)

	def update(self, instance, validated_data):
		"""updates and returns the user data"""
		password = validated_data.pop('password', None)
		user = super().update(instance, validated_data)
		if password:
			user.set_password(password)
			user.save()

		return user


#
class AuthTokenSerializer(serializers.Serializer):
	"""serializer for the user token"""
	email = serializers.EmailField()
	password = serializers.CharField(
		style={'input_type': 'password'},
		trim_whitespace=False,
	)

	def validate(self, attrs):
		"""
		It takes the email and password from the request,
		and then uses Django's built-in authenticate function to check if the
		user exists and if the password is correct

		:param attrs: the validated data from the serializer
		"""
		email = attrs.get('email')
		password = attrs.get('password')
		user = authenticate(
			request=self.context.get('request'),
			username=email,
			password=password
		)

		# Checking if the user is authenticated or not.
		if not user:
			msg = _('Unable to authenticate with provided credentials.')
			raise serializers.ValidationError(msg, code='authorization')

		# Returning the user object to the view.
		attrs['user'] = user
		return attrs
