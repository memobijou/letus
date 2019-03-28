from rest_framework import viewsets, serializers
from abc import ABCMeta, abstractmethod
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework import status
from offer.models import Offer, MemberOffer
from offer.serializers import OfferSerializer, ReadOnlyOfferSerializer, MemberOfferSerializer, \
    ReadOnlyMemberOfferSerializer, CreateOfferSerializer
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


class ReadOnlyOfferViewset(BaseOfferViewset, viewsets.ReadOnlyModelViewSet):
    serializer_class = ReadOnlyOfferSerializer


class MemberOfferViewset(viewsets.ModelViewSet):
    queryset = MemberOffer.objects.all()
    serializer_class = MemberOfferSerializer
    pagination_class = LimitOffsetPagination


class ReadOnlyMemberOfferViewset(viewsets.ReadOnlyModelViewSet):
    queryset = MemberOffer.objects.all()
    serializer_class = ReadOnlyMemberOfferSerializer
    pagination_class = LimitOffsetPagination


class OfferAPIView(APIView):
    def post(self, request, format=None):
        # title=creed&sub_title=apollo&organizer=1&member=2&datetime_from=2019-03-28T13:30&datetime_to=2019-03-28T13:30

        """
        get:
        A description of the get method on the custom action.

        post:
        paramters title, sub_title, organizer, member(many=True), datetime_from(many=True), datetime_to(many=True)
        """
        members = request.data.getlist("member")

        datetimes_from = request.data.getlist("datetime_from")
        datetimes_to = request.data.getlist("datetime_to")

        offer_serializer = CreateOfferSerializer(
            data=request.data, context={
                "members": members, "datetimes_from": datetimes_from, "datetimes_to": datetimes_to})

        if offer_serializer.is_valid():
            offer_serializer.save()
            return Response(offer_serializer.data, status=status.HTTP_201_CREATED)
        return Response(offer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
