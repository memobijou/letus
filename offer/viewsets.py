from rest_framework import viewsets
from abc import ABCMeta, abstractmethod

from rest_framework.pagination import LimitOffsetPagination

from offer.models import Offer
from offer.serializers import OfferSerializer


class BaseOfferViewset(viewsets.ModelViewSet, metaclass=ABCMeta):
    @property
    @abstractmethod
    def queryset(self):
        pass

    @property
    @abstractmethod
    def serializer_class(self):
        pass

    pagination_class = LimitOffsetPagination


class OfferViewset(BaseOfferViewset):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class ReadOnlyOfferViewset(BaseOfferViewset, viewsets.ReadOnlyModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
