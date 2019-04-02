from django.db.models import Prefetch, Q
from rest_framework import mixins
from offer.documents import offer_schema
from offer.models import Offer
from offer.serializers import OfferSerializer
from suggestion.models import Suggestion
from suggestion.serializers import SuggestionSerializer
from rest_framework.viewsets import GenericViewSet
from django.db.models import Count, Case, When, IntegerField


class OfferViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Offer.objects.prefetch_related(Prefetch(
        'offer_suggestions',
        queryset=Suggestion.objects.annotate(
            accepted_count=Count("responses__id", filter=Q(responses__accepted=True), distinct=True)
        ).order_by('-accepted_count')))
    serializer_class = OfferSerializer
    schema = offer_schema

    def get_queryset(self):
        if self.request.GET.get("member_id"):
            self.queryset = self.queryset.filter(members__id=self.request.GET.get("member_id")).distinct()
        return self.queryset


class OfferSuggestionViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                             mixins.UpdateModelMixin, GenericViewSet):
    queryset = Suggestion.objects.all()
    serializer_class = SuggestionSerializer

    def get_queryset(self):
        if self.kwargs.get("pk"):
            self.queryset = self.queryset.filter(id=self.kwargs.get("pk"))
        return self.queryset.filter(member_offer__offer_id=self.kwargs.get("offer_id"))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["offer_id"] = self.kwargs.get("offer_id", None)
        return context
