from rest_framework import viewsets
from rest_framework import status
from dw.filtres import OrderFilter
from dw.models import WalkOrder
from dw.serializers import WalkOrderSerializer
from django.core.exceptions import ValidationError
from rest_framework.response import Response

from django_filters import rest_framework as filters


class GetOrder(viewsets.ModelViewSet):
    queryset = WalkOrder.objects.all()
    serializer_class = WalkOrderSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = OrderFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_403_FORBIDDEN)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
