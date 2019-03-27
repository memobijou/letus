from django.urls import path, include
from rest_framework.routers import DefaultRouter
from suggestion.viewsets import SuggestionViewset

router = DefaultRouter()
router.register("suggestions", SuggestionViewset)

urlpatterns = [
    path("", include(router.urls))
]
