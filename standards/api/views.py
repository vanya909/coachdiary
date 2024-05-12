from rest_framework import mixins, viewsets, permissions, status
from django_filters import rest_framework as filters
from rest_framework.response import Response

from . import serializers
from . import filters as custom_filters
from .serializers import StudentStandardSerializer
from .. import models


class StandardValueViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = serializers.StandardValueSerializer
    queryset = models.StandardValue.objects.all()
    permission_classes = (
        permissions.IsAuthenticated,
    )


class StudentViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = serializers.StudentSerializer
    queryset = models.Student.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = custom_filters.StudentFilter
    permission_classes = (
        permissions.IsAuthenticated,
    )


class StudentClassViewset(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = serializers.StudentClassSerializer
    queryset = models.StudentClass.objects.all()
    permission_classes = (
        permissions.IsAuthenticated,
    )


class StudentStandardsViewSet(viewsets.ViewSet):
    def list(self, request, student_id=None):
        try:
            student = models.Student.objects.get(id=student_id)
        except models.Student.DoesNotExist:
            return Response({"error": "Студент не найден"}, status=status.HTTP_404_NOT_FOUND)

        student_standards = models.StudentStandard.objects.filter(student=student)
        serializer = StudentStandardSerializer(student_standards, many=True)
        return Response(serializer.data)