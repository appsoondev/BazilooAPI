"""
DATABASE Core models
"""
from django.contrib.auth.models import (
	AbstractBaseUser,
	BaseUserManager,
	PermissionsMixin,
)
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from app import settings


class UserManager(BaseUserManager):
	"""
	The UserManager class is a helper class,
	that provides a lot of functionality for creating and working with users.
	"""

	def create_user(self, email, password=None, **extra_fields):
		"""Create, save and return a new user."""

		if not email:
			raise ValueError("User MUST have an email address")

		user = self.model(email=self.normalize_email(email), **extra_fields)
		user.set_password(password)
		user.save(using=self._db)

		return user

	def create_superuser(self, email, password):
		"""Create and return a new superuser"""
		user = self.create_user(email, password)
		user.is_superuser = True
		user.is_staff = True
		user.save(using=self._db)

		return user


class User(AbstractBaseUser, PermissionsMixin):
	"""user in the system."""

	email = models.EmailField(max_length=255, unique=True)
	name = models.CharField(max_length=255)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	objects = UserManager()

	USERNAME_FIELD = 'email'

	def __str__(self):
		return self.name


class Lead(models.Model):
	"""Basic Lead model"""

	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
	)  # the user is the owner of the lead

	fname = models.CharField(max_length=255)
	lname = models.CharField(max_length=255)
	email = models.EmailField()
	phone = PhoneNumberField()
	ip = models.GenericIPAddressField(blank=True, null=True)

	def __str__(self):
		return self.email
