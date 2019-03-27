from django.urls import path, include
from rest_framework.routers import DefaultRouter
from member.viewsets import MemberViewset

router = DefaultRouter()
router.register("members", MemberViewset)

urlpatterns = [
    path("", include(router.urls))
]
