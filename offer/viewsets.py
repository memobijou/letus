from rest_framework import mixins

from rest_framework.generics import GenericAPIView
from rest_framework.pagination import LimitOffsetPagination
from offer.models import Offer
from offer.serializers import OfferSerializer


class OfferAPIView(mixins.CreateModelMixin, mixins.ListModelMixin, GenericAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
