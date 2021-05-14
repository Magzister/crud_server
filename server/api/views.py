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
from .permissions import IsUser
from rest_framework.response import Response
from .models import Access
from .models import AccessOffer
from .serializers import AccessSerializer
from .serializers import AccessOfferSerializer
from rest_framework.views import APIView
from rest_framework import status


class AccessList(generics.DestroyAPIView):
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

    def post(self, request, pk, format=None):
        access_offer = AccessOffer.objects.get(pk=pk)
        if access_offer.user == self.request.user:
            owner = access_offer.owner
            object = access_offer.object
            user = access_offer.user
            access = Access(
                user=user,
                object=object,
                owner=owner
            )
            access.save()
            access_offer.delete()
            return Response(status=status.HTTP_200_OK)
        data = {
            "detail": "You do not have permission to perform this action."
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class AccessOfferList(generics.DestroyAPIView):
    queryset = AccessOffer.objects.all()
    serializer_class = AccessOfferSerializer
    permission_classes = [IsAuthenticated, IsUser]

    def get(self, request, format=None):
        access_requests = AccessOffer.objects.filter(user=self.request.user)
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


class UserListWithNoAccess(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, object_pk, format=None):
        users = User.objects.exclude(
            user_accesses__object_id=object_pk
        ).exclude(
            user_access_offers__object_id=object_pk
        ).exclude(
            pk=self.request.user.id
        )
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Invite(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, user_pk, object_pk, format=None):
        object = Object.objects.get(id=object_pk)
        owner = self.request.user
        if object.owner == owner:
            access_offer = AccessOffer(
                user_id=user_pk,
                object_id=object_pk,
                owner_id=owner.id
            )
            access_offer.save()
            return Response(status=status.HTTP_200_OK)
        data = {
            "detail": "You do not have permission to perform this action."
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
