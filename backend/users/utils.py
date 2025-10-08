import jwt
from datetime import datetime, timedelta
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from django.conf import settings
# Secret key for signing the JWTs
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"

def generate_jwt(payload, expires_in=3600):
    """
    Generate a JWT token.

    Args:
        payload (dict): The data to encode in the token.
        expires_in (int): Expiration time in seconds (default is 1 hour).

    Returns:
        str: The generated JWT token.
    """
    payload['exp'] = datetime.utcnow() + timedelta(seconds=expires_in)
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_jwt(token):
    """
    Verify a JWT token.

    Args:
        token (str): The JWT token to verify.

    Returns:
        dict: The decoded payload if the token is valid.

    Raises:
        ExpiredSignatureError: If the token has expired.
        InvalidTokenError: If the token is invalid.
    """
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    except ExpiredSignatureError:
        raise ExpiredSignatureError("The token has expired.")
    except InvalidTokenError:
        raise InvalidTokenError("The token is invalid.")


def check_permission(decoded_token, required_permission):
    """
    Check if the user has the required permission.

    Args:
        decoded_token (dict): The decoded JWT payload.
        required_permission (str): The required permission to check.

    Returns:
        bool: True if the user has the required permission, False otherwise.
    """
    permissions = decoded_token.get("permissions", [])
    return required_permission in permissions


def get_user_from_token(decoded_token):
    """
    Retrieve user details from a decoded JWT token.

    Args:
        decoded_token (dict): The decoded JWT payload.

    Returns:
        dict: A dictionary containing user details (e.g., user_id, username).
    """
    user_id = decoded_token.get("user_id")
    username = decoded_token.get("username")
    return {"user_id": user_id, "username": username}


def get_user_id_from_request(request):
    """
    Extract the user ID from the JWT token in the request headers.

    Args:
        request (HttpRequest): Django request object.

    Returns:
        int | None: The user ID if token is valid, None otherwise.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None

    try:
        # Expecting header: "Bearer <token>"
        prefix, token = auth_header.split()
        if prefix.lower() != "bearer":
            return None

        decoded = verify_jwt(token)
        return decoded.get("user_id")
    except (ValueError, ExpiredSignatureError, InvalidTokenError):
        return None