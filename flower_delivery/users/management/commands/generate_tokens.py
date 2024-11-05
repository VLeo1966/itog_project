from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
user = User.objects.get(username='Valera1')
token, created = Token.objects.get_or_create(user=user)
print(token.key)  # используйте этот токен для авторизации в боте
