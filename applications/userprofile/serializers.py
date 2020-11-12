from django.contrib.auth.models import User
from rest_auth.serializers import PasswordResetSerializer
from rest_framework import serializers

from applications.userprofile.models import UserProfile
from applications.utils.utils import send_activation_email


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['username'] = validated_data['email']
        validated_data['is_active'] = False

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CreateUserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['user']

    def create(self, validated_data):
        user = UserSerializer().create(validated_data.get('user'))
        userprofile = UserProfile.objects.create(user=user)
        send_activation_email(user_pk=userprofile.id)
        return userprofile


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['user', 'id', 'created_date']


class ResetPasswordSerializer(PasswordResetSerializer):

    def get_email_options(self):
        return {'email_template_name': 'reset_password_email.html'}
