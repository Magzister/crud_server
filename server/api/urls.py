from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import MyObtainTokenPairView
from .views import RegisterView
from .views import UserList
from .views import UserDetail
from .views import ObjectDetail
from .views import ObjectList
from .views import AccessOfferList
from .views import AccessList
from .views import UserListWithNoAccess
from .views import Invite

urlpatterns = [
    path('objects/', ObjectList.as_view()),
    path('objects/<int:pk>/', ObjectDetail.as_view()),
    path('auth/login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('auth/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('users/', UserList.as_view(), name='user_list'),
    path('users/no-access/<int:object_pk>', UserListWithNoAccess.as_view(), name='users_with_no_access'),
    path('users/<int:user_pk>/invite/<int:object_pk>', Invite.as_view(), name='invite'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user_detail'),
    path('accesses/<int:object_pk>/', AccessList.as_view(), name='access_list'),
    path('accesses/offers/', AccessOfferList.as_view(), name='user_access_offers'),
    path('accesses/offers/<int:pk>', AccessOfferList.as_view()),
    path('accesses/accept/<int:pk>', AccessList.as_view(), name='accept_offer'),
]