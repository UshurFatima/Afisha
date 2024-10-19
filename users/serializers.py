from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import ConfirmCode


class UserBaseSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField()


class UserAuthSerializer(UserBaseSerializer):
    pass


class UserCreateSerializer(UserBaseSerializer):

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except:
            return username
        raise ValidationError('User already exists!')

    def validate_email(self, email):
        try:
            User.objects.get(email=email)
        except:
            return email
        raise ValidationError('User with this email already exists!')


class ConfirmCodeSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=1)
    code = serializers.CharField(max_length=6, min_length=6)

    def validate_user_id(self, user_id):
        try:
            ConfirmCode.objects.get(user_id=user_id)
        except ConfirmCode.DoesNotExist:
            raise ValidationError('There is no user with this id')

        return user_id
