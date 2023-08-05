from django.contrib.auth import get_user_model
from chowkidar.models import RefreshToken

UserModel = get_user_model()


def generate_refresh_token(userID: str) -> RefreshToken:
    return RefreshToken.objects.create(user_id=userID)


__all__ = [
    'generate_refresh_token'
]
