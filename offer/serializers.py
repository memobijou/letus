from rest_framework import serializers
from letus.serializers import CustomField, ModelDocument
from member.serializers import MemberSerializer
from offer.models import Offer, MemberOffer
from suggestion.serializers import SuggestionSerializer
from django.db import transaction


class MinimalOfferSerializer(serializers.ModelSerializer):
    organizer = MemberSerializer()

    class Meta:
        model = Offer
        fields = ("pk", "title", "sub_title", "organizer", "is_finished", "is_canceled", )


class MemberOfferSerializer(serializers.ModelSerializer):
    suggestions = SuggestionSerializer(many=True, required=False)
    extra_kwargs = {"member": {"allow_null": False}}

    class Meta:
        model = MemberOffer
        fields = ("pk", "offer", "member", "is_admin", "is_member", "suggestions", )


class BaseOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ("title", "sub_title", "organizer", "is_finished", "is_canceled", "offer_members", )


class OfferSerializer(ModelDocument, BaseOfferSerializer):
    offer_members = MemberOfferSerializer(many=True)
    suggestions = CustomField(initial=[], write_only=True,
                              help_text='List of dictionaries containing datetime_from and datetime_to')

    class Meta(BaseOfferSerializer.Meta):
        fields = BaseOfferSerializer.Meta.fields + ('suggestions',)

    @transaction.atomic
    def create(self, validated_data):
        offer_members = validated_data.pop("offer_members")
        suggestions = validated_data.pop("suggestions")

        instance = Offer.objects.create(**validated_data)

        organizer_offer_member_serializer = MemberOfferSerializer(
            data={"member": instance.organizer.pk, "offer": instance.pk, "is_admin": True, "is_member": True})

        if organizer_offer_member_serializer.is_valid():
            organizer_offer_member_instance = organizer_offer_member_serializer.save()
        else:
            raise serializers.ValidationError(organizer_offer_member_serializer.errors)

        for suggestion in suggestions:
            suggestion_serializer = SuggestionSerializer(
                data={"member_offer": organizer_offer_member_instance.pk,
                      "datetime_from": suggestion.get("datetime_from", None),
                      "datetime_to": suggestion.get("datetime_to", None)})
            if suggestion_serializer.is_valid():
                suggestion_serializer.save()
            else:
                raise serializers.ValidationError(suggestion_serializer.errors)

        for offer_member in offer_members:
            member = getattr(offer_member.get("member", None), "pk", None)
            offer_member_serializer = MemberOfferSerializer(
                data={"offer": instance.pk, "is_member": True, "member": member})

            if offer_member_serializer.is_valid():
                offer_member_serializer.save()
            else:
                raise serializers.ValidationError(offer_member_serializer.errors)
        return instance

    @staticmethod
    def validate_suggestions(data):
        if len(data) == 0:
            raise serializers.ValidationError("You have to make at least one suggestion")
        return data
