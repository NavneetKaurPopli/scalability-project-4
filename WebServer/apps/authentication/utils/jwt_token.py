from datetime import datetime, timedelta
import jwt
from django.conf import settings
 
def generate_jwt_token(username):
    """
    Generates a JSON Web Token that stores this user's ID and has an expiry
    date set to 60 days into the future.
    """
    dt = datetime.now() + timedelta(days=60)

    token = jwt.encode({
        'username': username,
        'exp': int(dt.strftime('%S'))
    }, settings.SECRET_KEY, algorithm='HS256')

    return token.decode('utf-8')

