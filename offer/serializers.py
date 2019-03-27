from rest_framework import serializers
from member.serializers import MemberSerializer
from offer.models import Offer


class BaseOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ("title", "sub_title", "organizer")


class ReadOnlyOfferSerializer(BaseOfferSerializer):
    organizer = MemberSerializer(read_only=True)


class OfferSerializer(BaseOfferSerializer):
    pass
