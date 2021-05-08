from django.urls import path
from .views import ObjectList
from .views import ObjectDetail
from rest_framework_simplejwt.views import TokenRefreshView
from api.views import MyObtainTokenPairView, RegisterView, UserList, UserDetail

urlpatterns = [
    path('objects/', ObjectList.as_view()),
    path('objects/<int:pk>/', ObjectDetail.as_view()),
    path('auth/login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('auth/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('api/users/', UserList.as_view(), name='user_list'),
    path('api/users/<int:pk>/', UserDetail.as_view(), name='user_detail'),
]