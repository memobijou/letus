from suggestion.viewsets import MemberSuggestionResponseViewset, SuggestionViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("suggestions", SuggestionViewSet)
router.register(r"suggestions/(?P<suggestion_id>\d+)/responses", MemberSuggestionResponseViewset)

urlpatterns = router.urls
