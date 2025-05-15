from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.api.serializers import UserRegisterSerializer


class UserRegisterApiView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    status_code = status.HTTP_201_CREATED
    permission_classes = [AllowAny]

    def perform_create(self, serializer) -> None:
        user = serializer.save()
        token = RefreshToken.for_user(user)
        self.token = token.access_token
        self.refresh_token = token

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(status=self.status_code, data={'refresh': str(self.refresh_token), 'access': str(self.token)})
