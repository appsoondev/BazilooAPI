"""
Django admin customisation
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from . import models


class UserAdmin(BaseUserAdmin):
	"""Define the admin pages for users"""
	ordering = ['id']
	list_display = ['email', 'name', ]
	readonly_fields = ['last_login', ]

	fieldsets = (
		# Email, Password
		(None, {'fields': ('email', 'password')}),
		# Permissions
		(
			_('Permissions'),
			{
				'fields':
					('is_staff',
					 'is_active',
					 'is_superuser',
					 )
			}
		),
		# Dates
		(_('Important Dates'), {'fields': ('last_login',)}),

	)

	add_fieldsets = (
		(
			None,
			{
				'classes': ('wide',),
				'fields':  (
					'email',
					'password1',
					'password2',
					'name',
					'is_active',
					'is_staff',
					'is_superuser',
				)
			}
		),
	)


# Registering the User model with the UserAdmin class.
admin.site.register(models.User, UserAdmin)
# Registering the Lead model to the admin site.
admin.site.register(models.Lead)
