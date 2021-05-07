from django.urls import path
from .views import ObjectList
from .views import ObjectDetail
from rest_framework_simplejwt.views import TokenRefreshView
from api.views import MyObtainTokenPairView, RegisterView, UserAPIView

urlpatterns = [
    path('objects/', ObjectList.as_view()),
    path('objects/<int:pk>/', ObjectDetail.as_view()),
    path('auth/login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('auth/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('api/user/', UserAPIView.as_view(), name='user'),
]