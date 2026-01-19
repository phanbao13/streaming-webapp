from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ("email", "password")
    
    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role="VIEWER",
        )
    
    def to_representation(self, instance):
        # after create user, return JWT
        refresh = RefreshToken.for_user(instance)
        return {
            "user": {
                "id": instance.id,
                "email": instance.email,
                "role": instance.role,
            },
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "role", "created_at")