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
from rest_framework.decorators import api_view
from django.db.models import Q
from .models import QRCode
from .serializers import QRCodeSerializer
from django.utils.timezone import utc

import json
import datetime
import hashlib


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


class UserAccessList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        accesses = Access.objects.filter(user=self.request.user)
        serializer = AccessSerializer(accesses, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_access_key(request, object_pk):
    user = request.user
    if bool(user and user.is_authenticated):
        object = Object.objects.get(pk=object_pk)
        is_owner = (object.owner == user)
        access = Access.objects.filter(Q(user=user) & Q(object=object))
        if len(access) > 1:
            serializer = AccessSerializer(access, many=True)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        is_have_access = bool(access)
        if is_owner or is_have_access:
            hash = hashlib.sha256()
            time = datetime.datetime.now().strftime('%m%d%Y%H%M%S')
            hash_str = bytes(time, 'utf-8') + bytes(user.username, 'utf-8') + bytes(object.name, 'utf-8')
            hash.update(hash_str)
            code = hash.hexdigest()
            data = {
                "code": code
            }
            qr_code = QRCode(
                user=user,
                object=object,
                code=code
            )
            qr_code.save()
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                "detail": "You do not have permission to perform this action."
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    else:
        data = {
            "detail": "You do not have permission to perform this action."
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_access_with_key(request, object_pk):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    code = data['code']
    object = Object.objects.get(pk=object_pk)
    qr_code = QRCode.objects.filter(Q(code=code) & Q(object=object))
    if len(qr_code) > 1:
        serializer = QRCodeSerializer(qr_code, many=True)
        return Response(serializer.data, status=status.HTTP_501_NOT_IMPLEMENTED)
    if not qr_code:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    created = qr_code[0].created
    if (now - created).total_seconds() > 60:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)
