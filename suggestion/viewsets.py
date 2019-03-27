from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from suggestion.models import Suggestion
from suggestion.serializers import SuggestionSerializer


class SuggestionViewset(viewsets.ModelViewSet):
    queryset = Suggestion.objects.all()
    serializer_class = SuggestionSerializer
    pagination_class = LimitOffsetPagination
