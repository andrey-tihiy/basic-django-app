from django.urls import path
from rest_framework import routers

from applications.userprofile.views import (
    CreateUserProfileView,
    UserProfileViewSet,
    ActivateUserAPIView,
    CurrentUserProfileViewSet,
)


router = routers.SimpleRouter(trailing_slash=False)
router.register(r'userprofile', UserProfileViewSet, basename='userprofiles')

urlpatterns = [
    path('current/', CurrentUserProfileViewSet.as_view(), name='current-user'),
    path('create-userprofile/', CreateUserProfileView.as_view(), name='create-userprofile'),
    path('activate-userprofile/', ActivateUserAPIView.as_view(), name='activate-userprofile'),
]

urlpatterns += router.urls
