"""Urls mapping for the lead app"""

from django.urls import (include, path)
from lead import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register('lead', views.LeadViewSet)

app_name = 'lead'

urlpatterns = [
	path('', include(router.urls))
]
