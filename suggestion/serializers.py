from rest_framework import serializers
from offer.models import MemberOffer
from suggestion.models import Suggestion, MemberSuggestionResponse
from django.db import transaction


class BaseSuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suggestion
        fields = ("pk", "member_offer", "datetime_from", "datetime_to",)
        extra_kwargs = {'datetime_from': {'allow_null': False}, "datetime_to": {"allow_null": False}}


class SuggestionSerializer(serializers.ModelSerializer):
    offer = serializers.IntegerField(source="member_offer.offer_id", read_only=True)
    member = serializers.IntegerField(source="member_offer.member_id")

    class Meta(BaseSuggestionSerializer.Meta):
        fields = ("member", "datetime_from", "datetime_to", "offer", )

    @transaction.atomic
    def create(self, validated_data, pk=None):
        member_offer = validated_data.pop("member_offer")
        member_id = member_offer.pop("member_id")
        offer_id = self.context.get("offer_id", None)

        try:
            member_offer_instance = MemberOffer.objects.get(member_id=member_id, offer_id=offer_id)
        except MemberOffer.DoesNotExist:
            raise serializers.ValidationError("Member not existing in that offer")

        validated_data["member_offer"] = member_offer_instance
        instance = Suggestion.objects.create(**validated_data)
        return instance


class MemberSuggestionResponseSerializer(serializers.ModelSerializer):
    suggestion_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = MemberSuggestionResponse
        fields = ("pk", "member", "accepted", "suggestion_id")

    @transaction.atomic
    def create(self, validated_data):
        suggestion_id = self.context.get("suggestion_id", None)
        if suggestion_id:
            validated_data["suggestion_id"] = suggestion_id
        instance = MemberSuggestionResponse.objects.create(**validated_data)
        return instance
