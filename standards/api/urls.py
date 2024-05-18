from django.urls import include, path
from rest_framework import routers

from . import views

standards_router = routers.DefaultRouter()
standards_router.register(r"standards", views.StandardValueViewSet, basename="students-standards")
standards_router.register(r"students", views.StudentViewSet, basename="students")
standards_router.register(r"classes", views.StudentClassViewset, basename="classes")
standards_router.register(r"students/(?P<student_id>\d+)/standards", views.StudentStandardsViewSet,
                          basename="student-standards")

urlpatterns = [
    path("", include(standards_router.urls)),
]
