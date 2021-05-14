from rest_framework import serializers
from .models import Object
from .models import QRCode
from .models import AccessOffer
from .models import Access
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name')


class ObjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Object
        fields = ['id', 'name', 'owner', 'description']


class AccessSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    object = ObjectSerializer(read_only=True)

    class Meta:
        model = Access
        fields = ['user', 'object']


class AccessOfferSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    object = ObjectSerializer(read_only=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = AccessOffer
        fields = ['id', 'user', 'owner', 'object']


class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = ['id', 'object', 'code', 'status']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        errors_dict = {}

        if attrs['password'] != attrs['password2']:
            errors_dict["password2"] = "Password fields didn't match."
        if not attrs['first_name']:
            errors_dict["first_name"] = "This field may not be blank."
        if not attrs['last_name']:
            errors_dict["last_name"] = "This field may not be blank."

        if errors_dict:
            raise serializers.ValidationError(errors_dict)

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
