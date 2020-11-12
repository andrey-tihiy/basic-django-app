from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework import permissions
from rest_framework import filters
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from applications.userprofile.models import UserProfile
from applications.userprofile.serializers import CreateUserProfileSerializer, UserProfileSerializer


class CreateUserProfileView(CreateAPIView):
    queryset = UserProfile.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CreateUserProfileSerializer


class UserProfileViewSet(ListModelMixin, UpdateModelMixin, DestroyModelMixin, RetrieveAPIView, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    ordering_fields = ['user__first_name', 'user__email', 'created_date']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'created_date']
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]

    def destroy(self, request, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(id=kwargs.get("pk"))
            profile.user.delete()
            return Response(status=HTTP_200_OK, data={'msg': "User Removed"})

        except ObjectDoesNotExist as e:
            return Response(status=HTTP_400_BAD_REQUEST, data={'error': e.__str__()})


class ActivateUserAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, *args, **kwargs):
        """User activation by provided uid and token"""
        token = self.request.data.get('token')

        try:
            userprofile = UserProfile.objects.get(id=token)
            user = userprofile.user
            userprofile.active = True
            user.is_active = True
            userprofile.save()
            user.save()

            return Response(status=HTTP_200_OK, data={'msg': "User activated"})
        except ObjectDoesNotExist as e:
            return Response(status=HTTP_400_BAD_REQUEST, data={'error': e.__str__()})


class CurrentUserProfileViewSet(RetrieveAPIView):
    queryset = UserProfile.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user.userprofile)
        return Response(serializer.data)
