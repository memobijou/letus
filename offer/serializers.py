from rest_framework import serializers
from abc import ABCMeta, abstractmethod

from offer.models import Offer


class BaseOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ("title", "sub_title")


class ReadOnlyOfferSerializer(BaseOfferSerializer):
    pass


class OfferSerializer(BaseOfferSerializer):
    pass
