from .models import Object
from .serializers import ObjectSerializer
from rest_framework import generics
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from .serializers import UserSerializer
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated


class ObjectList(generics.ListCreateAPIView):
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer


class ObjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
