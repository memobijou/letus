from django.urls import path, include
from offer.viewsets import OfferViewSet, OfferSuggestionViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("offers", OfferViewSet)
router.register(r"offers/(?P<offer_id>\d+)/suggestions", OfferSuggestionViewSet)


urlpatterns = router.urls
