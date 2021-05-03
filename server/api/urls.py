from django.urls import path
from .views import ObjectList
from .views import ObjectDetail

urlpatterns = [
    path('objects/', ObjectList.as_view()),
    path('objects/<int:pk>/', ObjectDetail.as_view()),
]