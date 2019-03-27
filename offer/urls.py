from django.urls import path, include
from rest_framework.routers import DefaultRouter
from offer.viewsets import OfferViewset, ReadOnlyOfferViewset

router = DefaultRouter()
router.register("offers", OfferViewset)
router.register("read-offers", ReadOnlyOfferViewset)


urlpatterns = [
    path("", include(router.urls))
]
