from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from suggestion.models import MemberSuggestionResponse, Suggestion
from suggestion.serializers import MemberSuggestionResponseSerializer, SuggestionSerializer


class MemberSuggestionResponseViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                                      mixins.UpdateModelMixin, GenericViewSet):
    serializer_class = MemberSuggestionResponseSerializer
    queryset = MemberSuggestionResponse.objects.all()

    def get_object(self):
        return self.queryset.get(pk=self.kwargs.get("pk"))

    def get_queryset(self):
        return self.queryset.filter(suggestion_id=self.kwargs.get("suggestion_id"))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["suggestion_id"] = self.kwargs.get("suggestion_id")
        return context


class SuggestionViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Suggestion.objects.all()
    serializer_class = SuggestionSerializer

