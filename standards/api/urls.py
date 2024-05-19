from django.urls import include, path
from rest_framework import routers

from . import views
from .views import StudentsResultsViewSet

standards_router = routers.DefaultRouter()
standards_router.register(r"standards", views.StandardValueViewSet, basename="students-standards")
standards_router.register(r"students", views.StudentViewSet, basename="students")
standards_router.register(r"classes", views.StudentClassViewset, basename="classes")
standards_router.register(r"students/(?P<student_id>\d+)/standards", views.StudentStandardsViewSet,
                          basename="student-standards")
standards_router.register(r'students/results', StudentsResultsViewSet, basename='students-results')
standards_router.register(r'students/results/create', views.StudentResultsCreateViewSet,
                          basename='students-results-create')
standards_router.register(r'students/results/update', views.StudentResultsUpdateViewSet,
                          basename='students-results-update')

urlpatterns = [
    path("", include(standards_router.urls)),

]
