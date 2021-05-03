from .models import Object
from .serializers import ObjectSerializer
from rest_framework import generics


class ObjectList(generics.ListCreateAPIView):
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer


class ObjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer
