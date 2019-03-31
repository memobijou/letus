from django.urls import path, include
from rest_framework.routers import DefaultRouter
from offer.viewsets import OfferViewset, OfferAPIView

router = DefaultRouter()
router.register("offers", OfferViewset)

urlpatterns = [
    path("", include(router.urls),),
    path("offers/creation", OfferAPIView.as_view())
]
