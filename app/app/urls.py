"""
This is the main urls.py file.
It is used to route the requests to the appropriate apps views.
 """
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


# A list of URL patterns.
urlpatterns = [
	# This is the default Django admin site.
	path('admin/', admin.site.urls),

	# This is a path to the API schema.
	path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
	# This is a path to the API docs.
	path(
		'api/docs/',
		SpectacularSwaggerView.as_view(url_name='api-schema'),
		name='api-docs',
	),
	# Including the urls.py file in the user app.
	path('api/user/', include('user.urls'), name='user-api'),
	# Including the urls.py file in the lead app.
	path('api/lead/', include('lead.urls'), name='lead-api'),

]
