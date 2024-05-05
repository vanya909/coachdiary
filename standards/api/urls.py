from django.urls import include, path
from rest_framework import routers

from . import views

standards_router = routers.DefaultRouter()
standards_router.register(r"standards", views.StandardValueViewSet)

urlpatterns = [
    path("", include(standards_router.urls)),
]
