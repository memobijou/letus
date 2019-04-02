from rest_framework import serializers
from offer.models import MemberOffer
from suggestion.models import Suggestion, MemberSuggestionResponse
from django.db import transaction


class MemberSuggestionResponseSerializer(serializers.ModelSerializer):
    suggestion_id = serializers.IntegerField()
    member_id = serializers.IntegerField()

    class Meta:
        model = MemberSuggestionResponse
        fields = ("pk", "member_id", "accepted", "suggestion_id")

    @transaction.atomic
    def create(self, validated_data):
        print(f"hey: {validated_data}")
        suggestion_id = self.context.get("suggestion_id", None)
        if suggestion_id:
            validated_data["suggestion_id"] = suggestion_id
        instance = MemberSuggestionResponse.objects.create(**validated_data)
        return instance


class BaseSuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suggestion
        fields = ("pk", "member_offer", "datetime_from", "datetime_to",)
        extra_kwargs = {'datetime_from': {'allow_null': False}, "datetime_to": {"allow_null": False}}


class SuggestionSerializer(serializers.ModelSerializer):
    offer_id = serializers.IntegerField(source="member_offer.offer_id", read_only=True)
    member_id = serializers.IntegerField(source="member_offer.member_id")
    responses = MemberSuggestionResponseSerializer(read_only=True, many=True)

    class Meta(BaseSuggestionSerializer.Meta):
        fields = ("pk", "member_id", "datetime_from", "datetime_to", "offer_id", "responses")

    @transaction.atomic
    def create(self, validated_data):
        print(f"blabla: {validated_data}")
        member_offer = validated_data.pop("member_offer")
        member_id = member_offer.get("member_id", None)
        offer_id = self.context.get("offer_id", None)

        try:
            member_offer_instance = MemberOffer.objects.get(member_id=member_id, offer_id=offer_id)
        except MemberOffer.DoesNotExist:
            raise serializers.ValidationError("Member not existing in that offer")

        validated_data["member_offer"] = member_offer_instance
        instance = Suggestion.objects.create(**validated_data)
        return instance
