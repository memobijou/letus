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

    class Meta:
        model = MemberOffer
        fields = ("pk", "offer", "member", "is_admin", "is_member", "suggestions", )


class BaseOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ("title", "sub_title", "organizer", "is_finished", "is_canceled", "members_offers", )


class OfferSerializer(ModelDocument, BaseOfferSerializer):
    members_offers = MemberOfferSerializer(many=True)
    suggestions = CustomField(initial=[], write_only=True,
                              help_text='List of dictionaries containing datetime_from and datetime_to')

    class Meta(BaseOfferSerializer.Meta):
        fields = BaseOfferSerializer.Meta.fields + ('suggestions',)

    @transaction.atomic
    def create(self, validated_data):
        print("???????????")
        members_offers = validated_data.pop("members_offers")
        suggestions = validated_data.pop("suggestions")

        instance = Offer.objects.create(**validated_data)

        members_offers_serializers = [MemberOfferSerializer(
            data={"member": instance.organizer.pk, "offer": instance.pk, "is_admin": True})]
        for member_offer in members_offers:
            members_offers_serializers.append(MemberOfferSerializer(
                data={"offer": instance.pk, "is_member": True, "member": member_offer["member"].pk}))

        for members_offers_serializer in members_offers_serializers:
            if members_offers_serializer.is_valid():
                members_offers_instance = members_offers_serializer.save()
                if members_offers_instance.is_admin is True:
                    for suggestion in suggestions:
                        suggestion_serializer = SuggestionSerializer(
                            data={"member_offer": members_offers_instance.pk,
                                  "datetime_from": suggestion.get("datetime_from", None),
                                  "datetime_to": suggestion.get("datetime_to", None)})
                        if suggestion_serializer.is_valid():
                            suggestion_serializer.save()
                        else:
                            raise serializers.ValidationError(suggestion_serializer.errors)
            else:
                raise serializers.ValidationError(members_offers_serializer.errors)
        return instance

    @staticmethod
    def validate_suggestions(data):
        if len(data) == 0:
            raise serializers.ValidationError("You have to make at least one suggestion")
        return data


class CreateOfferSerializer(BaseOfferSerializer):
    members_offers = MemberOfferSerializer(many=True, read_only=True)

    def create(self, validated_data):
        instance = Offer.objects.create(**validated_data)

        organizer = self.validated_data.get("organizer")

        datetimes_from = self.context.get("datetimes_from")
        datetimes_to = self.context.get("datetimes_to")

        member_ids = self.context.get("members")

        organizer_member_offer_serializer = MemberOfferSerializer(
            data={"member": organizer.pk, "offer": instance.pk, "is_admin": True, "is_member": True})

        members_member_offer_serializers = [
            MemberOfferSerializer(data={"member": member_id, "offer": instance.pk, "is_member": True}) for member_id in member_ids
        ]

        errors = {}

        if organizer_member_offer_serializer.is_valid():
            organizer_member_offer_instance = organizer_member_offer_serializer.save()
            self.create_organizer_suggestions(datetimes_from, datetimes_to, organizer_member_offer_instance, errors)
        else:
            self.add_serializers_error_messages_to_errors(organizer_member_offer_serializer, errors)

        for members_member_offer_serializer in members_member_offer_serializers:
            if members_member_offer_serializer.is_valid():
                members_member_offer_serializer.save()
            else:
                self.add_serializers_error_messages_to_errors(members_member_offer_serializer, errors)
        if errors:
            raise serializers.ValidationError(errors)
        # instance.published = True
        # instance.save()
        return instance

    def create_organizer_suggestions(self, datetimes_from, datetimes_to, organizer_member_offer_instance, errors):
        if len(datetimes_from) == len(datetimes_to):
            for datetime_from, datetime_to in zip(datetimes_from, datetimes_to):
                suggestion_serializer = SuggestionSerializer(
                    data={"member_offer": organizer_member_offer_instance.pk, "datetime_from": datetime_from,
                          "datetime_to": datetime_to})
                if suggestion_serializer.is_valid():
                    suggestion_serializer.save()
                else:
                    self.add_serializers_error_messages_to_errors(suggestion_serializer, errors)

    @staticmethod
    def add_serializers_error_messages_to_errors(serializer, errors):
        for field, error_msg in serializer.errors.items():
            if field not in errors:
                errors[field] = []
            errors[field].append(error_msg)
