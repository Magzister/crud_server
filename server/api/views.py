from .models import Object
from .serializers import ObjectSerializer
from rest_framework import generics
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from rest_framework.response import Response


class ObjectList(generics.CreateAPIView):
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer
    permission_classes = [IsOwner]

    def get(self, request, format=None):
        objects = Object.objects.filter(owner=self.request.user)
        serializer = ObjectSerializer(objects, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ObjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer
    permission_classes = [IsOwner]


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
