from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from django.contrib.auth.models import User

from member.models import Member


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pk", "first_name", "last_name", "username", "email")
        extra_kwargs = {
            'username': {
                'validators': [UnicodeUsernameValidator()],
            }
        }


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

    def validate(self, data):
        username = data.get('user').get('username')
        self.validate_username_uniqueness(username)
        return data

    def validate_username_uniqueness(self, username):
        username_users = User.objects.filter(username=username)
        if self.instance:
            username_users = username_users.exclude(member__pk=self.instance.pk)
        if username_users.count() > 0:
            raise serializers.ValidationError("Dieser Benutzername existiert bereits.")
