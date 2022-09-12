import secrets

API_KEY_LEN = 32


def key_gen():
    """Generate a 32-char API Key"""
    return secrets.token_urlsafe(API_KEY_LEN)
