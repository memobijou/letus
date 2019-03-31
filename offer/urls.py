from django.urls import path
from offer.viewsets import OfferAPIView


urlpatterns = [
    path("offers/", OfferAPIView.as_view())
]
