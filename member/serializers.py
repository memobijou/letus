from rest_framework import serializers
from django.contrib.auth.models import User

from member.models import Member


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pk", "first_name", "last_name", "username", "email")


class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Member
        fields = ("user",)

    def create(self, validated_data):
        user = User.objects.create(**validated_data.get("user"))
        return user.member

    def update(self, instance, validated_data):
        User.objects.filter(pk=instance.user_id).update(**validated_data.get('user'))
        return instance
