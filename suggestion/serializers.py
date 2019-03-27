from rest_framework import serializers
from suggestion.models import Suggestion


class SuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suggestion
        fields = ("pk", "datetime_from", "datetime_to", )
