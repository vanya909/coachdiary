from rest_framework import mixins, viewsets, permissions

from . import serializers
from .. import models


class StandardValueViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
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
    viewsets.GenericViewSet,
):
    serializer_class = serializers.StudentSerializer
    queryset = models.Student.objects.all()
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
