from django.db.models import Prefetch
from rest_framework import mixins, viewsets, permissions, status
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from . import serializers
from . import filters as custom_filters
from .serializers import StudentStandardSerializer, StudentSerializer
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
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get_queryset(self):
        user = self.request.user
        return models.StandardValue.objects.filter(student_class__class_owner=user)


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
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return models.Student.objects.filter(student_class__class_owner=user)

    @action(detail=False, methods=['get'])
    def results(self, request):
        class_ids = request.query_params.getlist('class_id[]')
        standard_id = request.query_params.get('standard_id')

        if not class_ids or not standard_id:
            return Response({"error": "class_id[] and standard_id are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            standard = models.Standard.objects.get(id=standard_id)
        except models.Standard.DoesNotExist:
            return Response({"error": "Standard not found."}, status=status.HTTP_404_NOT_FOUND)

        students = models.Student.objects.filter(student_class__id__in=class_ids, student_class__class_owner=request.user)
        results = models.StudentStandard.objects.filter(student__in=students, standard=standard)

        response_data = []
        for result in results:
            student_data = StudentSerializer(result.student).data
            result_data = {
                "value": result.value,
                "grade": result.grade
            }
            student_data.update(result_data)
            response_data.append(student_data)

        return Response(response_data, status=status.HTTP_200_OK)


class StudentClassViewset(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = serializers.StudentClassSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get_queryset(self):
        user = self.request.user
        return models.StudentClass.objects.filter(class_owner=user)

    def get_object(self):
        obj = super().get_object()
        if obj.class_owner != self.request.user:
            raise PermissionDenied("You do not have permission to access this object.")
        return obj


class StudentStandardsViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, student_id=None):
        try:
            student = models.Student.objects.get(id=student_id, student_class__class_owner=request.user)
        except models.Student.DoesNotExist:
            raise PermissionDenied("You do not have permission to access this student's standards.")

        student_standards = models.StudentStandard.objects.filter(student=student)
        serializer = StudentStandardSerializer(student_standards, many=True)
        return Response(serializer.data)
