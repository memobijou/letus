from rest_framework import serializers
from member.serializers import MemberSerializer
from offer.models import Offer, MemberOffer


class MemberOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberOffer
        fields = ("pk", "offer", "member", "is_admin", )


class BaseOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ("title", "sub_title", "organizer", "is_finished", "is_canceled", "members_offers", )


class ReadOnlyOfferSerializer(BaseOfferSerializer):
    organizer = MemberSerializer()
    members_offers = MemberOfferSerializer(many=True)


class OfferSerializer(BaseOfferSerializer):
    members_offers = MemberOfferSerializer(many=True, read_only=True)
