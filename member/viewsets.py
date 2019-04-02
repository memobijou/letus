from rest_framework import viewsets

from member.models import Member
from member.serializers import MemberSerializer


class MemberViewSet(viewsets.ModelViewSet):
    serializer_class = MemberSerializer
    queryset = Member.objects.all()

