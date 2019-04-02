from rest_framework import serializers
from offer.models import MemberOffer
from suggestion.models import Suggestion, MemberSuggestionResponse
from django.db import transaction


class MemberSuggestionResponseSerializer(serializers.ModelSerializer):
    suggestion_id = serializers.IntegerField(required=False, allow_null=True)
    member_id = serializers.IntegerField(required=False, allow_null=True)

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
        fields = ("pk", "datetime_from", "datetime_to", "offer_id", "responses")
        extra_kwargs = {'datetime_from': {'allow_null': False}, "datetime_to": {"allow_null": False}}


class SuggestionSerializer(BaseSuggestionSerializer):
    offer_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    responses = MemberSuggestionResponseSerializer(read_only=True, many=True)

    @transaction.atomic
    def create(self, validated_data):
        print(validated_data)
        instance = Suggestion.objects.create(**validated_data)
        return instance
