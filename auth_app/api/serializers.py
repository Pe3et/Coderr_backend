from django.contrib.auth.models import User
from django.core.validators import validate_email
from rest_framework import serializers

from auth_app.api.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['type']


class RegistrationSerializer(serializers.ModelSerializer):
    
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(choices=UserProfile.TYPE_CHOICES, write_only=True)
    email = serializers.CharField()
    username = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    """
    Validates if the email isn't already registered or wrong format with custom error message.
    """
    def validate_email(self, value):
        try:
            validate_email(value)
        except:
            raise serializers.ValidationError(['E-Mail-Format ist ungültig.'])

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(['Diese E-Mail-Adresse ist bereits registriert.'])

        return value
    
    """
    Validates if the username already exists with custom error message.
    """
    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(['Dieser Benutzername ist bereits vergeben.'])
        return value
    
    """
    Validates if the repeated password input is correct.
    """
    def validate_password(self, value):
        if value != self.initial_data['repeated_password']:
            raise serializers.ValidationError(
                ['Das Passwort ist nicht gleich mit dem wiederholten Passwort.'])
        return value

    """
    Creates the user and also it's UserProfile with customer or business type.
    """
    def create(self, validated_data):
        profile_type = validated_data.pop('type')
        validated_data.pop('repeated_password')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, type=profile_type)

        return user