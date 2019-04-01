from rest_framework import mixins

from rest_framework.generics import GenericAPIView
from rest_framework.pagination import LimitOffsetPagination
from offer.models import Offer
from offer.serializers import OfferSerializer
from suggestion.models import Suggestion
from suggestion.serializers import SuggestionSerializer
from rest_framework.viewsets import GenericViewSet


class OfferAPIView(mixins.CreateModelMixin, mixins.ListModelMixin, GenericAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class OfferSuggestionViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Suggestion.objects.all()
    serializer_class = SuggestionSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return self.queryset.filter(member_offer__offer_id=self.kwargs.get("pk"))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["pk"] = self.kwargs.get("pk", None)
        print(f"sammy: {context['pk']}")
        return context
