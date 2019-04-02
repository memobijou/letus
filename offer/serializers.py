from rest_framework import serializers
from letus.serializers import CustomField, ModelDocument
from member.serializers import MemberSerializer
from offer.models import Offer, MemberOffer
from suggestion.serializers import SuggestionSerializer, MemberSuggestionResponseSerializer
from django.db import transaction


class MemberOfferSerializer(serializers.ModelSerializer):
    member = MemberSerializer(read_only=True)
    member_id = serializers.IntegerField()
    offer_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)
    extra_kwargs = {"member_id": {"allow_null": False}}

    class Meta:
        model = MemberOffer
        fields = ("offer_id", "member_id", "member", "is_admin", "is_member",)


class BaseOfferSerializer(serializers.ModelSerializer):
    organizer = MemberSerializer(read_only=True)
    organizer_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Offer
        fields = ("pk", "title", "sub_title", "organizer_id", "organizer", "is_finished", "is_canceled",
                  "offer_members", "offer_suggestions",)


class OfferSerializer(ModelDocument, BaseOfferSerializer):
    offer_members = MemberOfferSerializer(many=True)

    @transaction.atomic
    def create(self, validated_data):
        offer_members = validated_data.pop("offer_members")
        print(f"hallo {offer_members}")

        offer_suggestions = validated_data.pop("offer_suggestions")

        instance = Offer.objects.create(**validated_data)

        organizer_offer_member_serializer = MemberOfferSerializer(
            data={"member_id": instance.organizer_id, "offer_id": instance.pk, "is_admin": True, "is_member": True}
        )

        if organizer_offer_member_serializer.is_valid():
            organizer_offer_member_instance = organizer_offer_member_serializer.save()
        else:
            raise serializers.ValidationError(organizer_offer_member_serializer.errors)
        print("???")

        print(f"lie: {offer_members}")
        for offer_member in offer_members:
            member_id = offer_member.get("member_id", None)
            print(f"!!! {member_id}")
            offer_member_serializer = MemberOfferSerializer(
                data={"offer_id": instance.pk, "is_member": True, "member_id": member_id})

            if offer_member_serializer.is_valid():
                offer_member_serializer.save()
            else:
                raise serializers.ValidationError(offer_member_serializer.errors)

        offer_suggestion_instances = []
        for offer_suggestion in offer_suggestions:
            offer_suggestion_serializer = SuggestionSerializer(
                data={"member_id": organizer_offer_member_instance.member_id,
                      "datetime_from": offer_suggestion.get("datetime_from", None),
                      "datetime_to": offer_suggestion.get("datetime_to", None)}, context={"offer_id": instance.pk})
            if offer_suggestion_serializer.is_valid():
                offer_suggestion_instance = offer_suggestion_serializer.save()
                offer_suggestion_instances.append(offer_suggestion_instance)
            else:
                raise serializers.ValidationError(offer_suggestion_serializer.errors)

        print(offer_members)
        for offer_suggestion_instance in offer_suggestion_instances:
            for offer_member in offer_members:
                member_id = offer_member.get("member_id", None)
                print(f"why: {member_id} - {offer_suggestion_instance.id}")
                member_suggestion_response_serializer = MemberSuggestionResponseSerializer(
                    data={"member_id": member_id, "suggestion_id": offer_suggestion_instance.id})

                if member_suggestion_response_serializer.is_valid():
                    member_suggestion_response_serializer.save()
                else:
                    raise serializers.ValidationError(member_suggestion_response_serializer.errors)
        return instance

    @staticmethod
    def validate_suggestions(data):
        if len(data) == 0:
            raise serializers.ValidationError("You have to make at least one suggestion")
        return data
