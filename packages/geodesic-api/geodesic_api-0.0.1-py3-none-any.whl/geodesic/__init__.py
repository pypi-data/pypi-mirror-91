__version__ = '0.0.1'

from geodesic.oauth import AuthManager

def authenticate():
    auth = AuthManager()
    auth.authenticate()