from django.urls import path, include
from rest_framework.routers import DefaultRouter
from offer.viewsets import OfferViewset, ReadOnlyOfferViewset, MemberOfferViewset

router = DefaultRouter()
router.register("offers", OfferViewset)
router.register("read-offers", ReadOnlyOfferViewset)
router.register("members-offers", MemberOfferViewset)


urlpatterns = [
    path("", include(router.urls))
]
