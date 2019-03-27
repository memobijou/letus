from django.urls import path, include
from rest_framework.routers import DefaultRouter
from offer.viewsets import OfferViewset, ReadOnlyOfferViewset, MemberOfferViewset, ReadOnlyMemberOfferViewset

router = DefaultRouter()
router.register("offers", OfferViewset)
router.register("read-offers", ReadOnlyOfferViewset)
router.register("members-offers", MemberOfferViewset)
router.register("read-members-offers", ReadOnlyMemberOfferViewset)


urlpatterns = [
    path("", include(router.urls))
]
