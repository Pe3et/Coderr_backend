from django.contrib.auth.models import User
from django.core.validators import validate_email
from rest_framework import serializers

from auth_app.api.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = UserProfile
        exclude = ['id']

    """
    To handle the PATCH for a UserProfile with it's connected User
    """
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)
        user.save()
        return super().update(instance, validated_data)
    
    """
    Validates if the email isn't already registered or wrong format with custom error message.
    """
    def validate_email(self, value):
        try:
            validate_email(value)
        except:
            raise serializers.ValidationError(['E-Mail-Format ist ungültig.'])

        if self.instance and value != self.instance.user.email and User.objects.filter(email=value).exists():
            raise serializers.ValidationError(['Diese E-Mail-Adresse ist bereits registriert.'])

        return value
    
    """
    Raises 400 for bad requests.
    """
    def validate(self, data):
        if not data:
            raise serializers.ValidationError(['Ungültige oder fehlende Felder.'])
        return data


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