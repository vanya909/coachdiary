from rest_framework import mixins, viewsets, permissions

from .serializers import StandardValueSerializer
from ..models import StandardValue


class StandardValueViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = StandardValueSerializer
    queryset = StandardValue.objects.all()
    permission_classes = (
        permissions.IsAuthenticated,
    )
