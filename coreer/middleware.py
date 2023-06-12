from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework.authentication import TokenAuthentication
from channels.db import database_sync_to_async


# class TokenAuthMiddleware:
#     def __init__(self, inner):
#         self.inner = inner

#     async def __call__(self, scope, receive, send):
#         headers = dict(scope['headers'])
#         if b'authorization' in headers:
#             try:
#                 token_name, token_key = headers[b'authorization'].decode().split()
#                 if token_name == 'Token':
#                     knox_auth = TokenAuthentication()
#                     user, auth_token = await database_sync_to_async(knox_auth.authenticate_credentials)(token_key)
#                     scope['user'] = user
#                     close_old_connections()
#             except Token.DoesNotExist:
#                 scope['user'] = AnonymousUser()
#         return await self.inner(scope, receive, send)
from channels.middleware import BaseMiddleware

@database_sync_to_async
def get_user(token_key):
    try:
        print("FOUND USER")
        token = Token.objects.get(key=token_key)
        user = token.user
        print(user)
    except Exception:
        print("COULDNT FIND USER")
        user = None
    return user

class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        try:
            token_key = (dict((x.split('=') for x in scope['query_string'].decode().split("&")))).get('token', None)
        except ValueError:
            token_key = None
        scope['user'] = AnonymousUser() if token_key is None else await get_user(token_key)

        print("SUCCESS")
        return await super().__call__(scope, receive, send)