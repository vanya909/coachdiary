from django.urls import include, path
from rest_framework import routers

from . import views
from .views import StudentsByClassView, StandardsByClassView, ClassesByOwnerView, FilterOptionsView


standards_router = routers.DefaultRouter()
standards_router.register(r"standardes", views.StandardValueViewSet) #TODO: пока убрал, потом верни

urlpatterns = [
    path("", include(standards_router.urls)),
    path('students/', StudentsByClassView.as_view(), name='students_by_class'),
    path('standards/', StandardsByClassView.as_view(), name='standards_by_class'),
    path('classes/', ClassesByOwnerView.as_view(), name='classes_by_owner'),
    path('filters/', FilterOptionsView.as_view(), name='filter_options'),
]
