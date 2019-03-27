from rest_framework import serializers
from member.serializers import MemberSerializer
from offer.models import Offer, MemberOffer


class BaseOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ("title", "sub_title", "organizer", "is_finished", "is_canceled",)


class ReadOnlyOfferSerializer(BaseOfferSerializer):
    organizer = MemberSerializer(read_only=True)


class OfferSerializer(BaseOfferSerializer):
    pass


class MemberOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberOffer
        fields = ("pk", "offer", "member", "is_admin", )
