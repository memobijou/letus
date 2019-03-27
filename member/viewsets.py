from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from member.models import Member
from member.serializers import MemberSerializer


class MemberViewset(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    pagination_class = LimitOffsetPagination
