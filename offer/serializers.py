from rest_framework import serializers
from member.serializers import MemberSerializer
from offer.models import Offer, MemberOffer
from suggestion.serializers import SuggestionSerializer


class MemberOfferSerializer(serializers.ModelSerializer):
    suggestions = SuggestionSerializer(many=True, read_only=True)

    class Meta:
        model = MemberOffer
        fields = ("pk", "offer", "member", "is_admin", "suggestions", )


class MinimalOfferSerializer(serializers.ModelSerializer):
    organizer = MemberSerializer()

    class Meta:
        model = Offer
        fields = ("pk", "title", "sub_title", "organizer", "is_finished", "is_canceled", )


class ReadOnlyMemberOfferSerializer(serializers.ModelSerializer):
    suggestions = SuggestionSerializer(many=True, read_only=True)
    offer = MinimalOfferSerializer()
    member = MemberSerializer()

    class Meta:
        model = MemberOffer
        fields = ("pk", "offer", "member", "is_admin", "suggestions", )


class BaseOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ("title", "sub_title", "organizer", "is_finished", "is_canceled", "members_offers", )


class ReadOnlyOfferSerializer(BaseOfferSerializer):
    organizer = MemberSerializer()
    members_offers = MemberOfferSerializer(many=True)


class OfferSerializer(BaseOfferSerializer):
    members_offers = MemberOfferSerializer(many=True, read_only=True)
