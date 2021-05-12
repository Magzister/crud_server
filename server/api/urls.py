from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import MyObtainTokenPairView
from .views import RegisterView
from .views import UserList
from .views import UserDetail
from .views import ObjectDetail
from .views import ObjectList
from .views import AccessOfferOwnerList
from .views import AccessOfferUserList
from .views import AccessList

urlpatterns = [
    path('objects/', ObjectList.as_view()),
    path('objects/<int:pk>/', ObjectDetail.as_view()),
    path('auth/login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('auth/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('users/', UserList.as_view(), name='user_list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user_detail'),
    path('accesses/<int:object_pk>/', AccessList.as_view(), name='access_list'),
    path('accesses/requests/owner/', AccessOfferOwnerList.as_view(), name='owner_access_requests'),
    path('accesses/requests/user/', AccessOfferUserList.as_view(), name='user_access_requests'),
]