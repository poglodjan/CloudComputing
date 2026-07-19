# file to manage stuffs connected with authentication, mainly drive tokens, and connected with user stuff to backend
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import firebase_admin
from firebase_admin import auth
import logging

logger = logging.getLogger(__name__)

from django.contrib.auth.models import AnonymousUser

# Inicjalizujemy Firebase tylko raz
if not firebase_admin._apps:
    firebase_admin.initialize_app()


class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        logger.info(f"Authorization header: {auth_header}")

        if not auth_header:
            logger.warning("No Authorization header provided")
            return None

        if not auth_header.startswith("Bearer "):
            logger.warning("Invalid token format in Authorization header")
            raise AuthenticationFailed("Invalid token format")
        
        id_token = auth_header.split("Bearer ")[1]
        logger.info(f"Received token: {id_token[:20]}...")  # pokaż tylko początek tokena dla bezpieczeństwa

        try:
            decoded_token = auth.verify_id_token(id_token)
            logger.info(f"Decoded token uid: {decoded_token.get('uid')}")
        except Exception as e:
            logger.error(f"Invalid Firebase token: {e}")
            raise AuthenticationFailed("Invalid Firebase token") from e

        user = FirebaseUser(decoded_token)
        return (user, None)


class FirebaseUser:
    def __init__(self, decoded_token):
        self.uid = decoded_token.get("uid")
        self.email = decoded_token.get("email")
        self.name = decoded_token.get("name", "")
        self.token = decoded_token
        self.is_authenticated = True

    def __str__(self):
        return self.email or self.uid
