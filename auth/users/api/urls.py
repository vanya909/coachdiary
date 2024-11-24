from django.urls import path

from .views import UserLoginView, UserViewSet, UserProfileViewSet, UserLogoutView, get_pkce_params, vk_auth

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="UserLogin"),
    path("create-user/", UserViewSet.as_view({"post": "create"}), name="UserCreate"),
    path("profile/", UserProfileViewSet.as_view(), name="UserProfile"),
    path("logout/", UserLogoutView.as_view(), name="UserLogout"),
    path('api/pkce/', get_pkce_params),
    path('api/auth/vk/', vk_auth),
]

