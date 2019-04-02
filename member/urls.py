from rest_framework.routers import DefaultRouter

from member.viewsets import MemberViewSet

router = DefaultRouter()
router.register("members", MemberViewSet)

urlpatterns = router.urls
