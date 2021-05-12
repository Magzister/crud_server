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
from .permissions import IsAccessRequestCreator
from rest_framework.response import Response
from .models import Access
from .models import AccessOffer
from .serializers import AccessSerializer
from .serializers import AccessOfferSerializer
from rest_framework.views import APIView


class AccessList(APIView):
    queryset = Access.objects.all()
    serializer_class = AccessSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, object_pk, format=None):
        object = Object.objects.get(id=object_pk)
        if object.owner == self.request.user:
            accesses = Access.objects.filter(object_id=object.id)
            serializer = AccessSerializer(accesses, many=True)
            return Response(serializer.data)
        data = {
            "detail": "You do not have permission to perform this action."
        }
        return Response(data)


class AccessOfferUserList(APIView):
    queryset = AccessOffer.objects.all()
    serializer_class = AccessOfferSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        access_requests = AccessOffer.objects.filter(user=self.request.user)
        serializer = AccessOfferSerializer(access_requests, many=True)
        return Response(serializer.data)


class AccessOfferOwnerList(generics.CreateAPIView):
    queryset = AccessOffer.objects.all()
    serializer_class = AccessOfferSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get(self, request, format=None):
        access_requests = AccessOffer.objects.filter(owner=self.request.user)
        serializer = AccessOfferSerializer(access_requests, many=True)
        return Response(serializer.data)


class ObjectList(generics.CreateAPIView):
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer
    permission_classes = [IsAuthenticated]

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
