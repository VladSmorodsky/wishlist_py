from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed


@database_sync_to_async
def get_user_from_token(headers):
    auth_header = None
    for header, header_value in headers:
        if header == b'authorization':
            auth_header = header_value.decode()
            break
    if not auth_header:
        return AnonymousUser()
    token = auth_header.split('Bearer ')[1]
    try:
        validated_token = JWTAuthentication().get_validated_token(token)
        return JWTAuthentication().get_user(validated_token)
    except AuthenticationFailed:
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    """
    Custom middleware for checking authenticated user
    """

    async def __call__(self, scope, receive, send):
        headers = scope.get('headers', [])
        scope['user'] = await get_user_from_token(headers)
        return await super().__call__(scope, receive, send)
