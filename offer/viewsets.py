from rest_framework import viewsets
from abc import ABCMeta, abstractmethod

from rest_framework.pagination import LimitOffsetPagination

from offer.models import Offer, MemberOffer
from offer.serializers import OfferSerializer, ReadOnlyOfferSerializer, MemberOfferSerializer


class BaseOfferViewset(metaclass=ABCMeta):
    queryset = Offer.objects.all()

    @property
    @abstractmethod
    def serializer_class(self):
        pass

    pagination_class = LimitOffsetPagination


class OfferViewset(BaseOfferViewset, viewsets.ModelViewSet):
    serializer_class = OfferSerializer


class ReadOnlyOfferViewset(BaseOfferViewset, viewsets.ReadOnlyModelViewSet):
    serializer_class = ReadOnlyOfferSerializer


class MemberOfferViewset(viewsets.ModelViewSet):
    queryset = MemberOffer.objects.all()
    serializer_class = MemberOfferSerializer
    pagination_class = LimitOffsetPagination
