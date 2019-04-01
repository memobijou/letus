from django.urls import path, include
from offer.viewsets import OfferAPIView, OfferSuggestionViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("", OfferSuggestionViewSet)


urlpatterns = [
    path("offers/", OfferAPIView.as_view()),
    path("offers/<int:pk>/suggestions/", include(router.urls))
]
