from rest_framework import viewsets, serializers, mixins
from abc import ABCMeta, abstractmethod

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework import status
from offer.models import Offer, MemberOffer
from offer.serializers import OfferSerializer, CreateOfferSerializer
from suggestion.serializers import SuggestionSerializer


class BaseOfferViewset(metaclass=ABCMeta):
    queryset = Offer.objects.all()

    @property
    @abstractmethod
    def serializer_class(self):
        pass

    pagination_class = LimitOffsetPagination


class OfferViewset(BaseOfferViewset, viewsets.ModelViewSet):
    serializer_class = OfferSerializer


class OfferAPIView(mixins.CreateModelMixin, mixins.ListModelMixin, GenericAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
