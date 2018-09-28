import cryptography.fernet

from config import get_config

config = get_config('security', sensitive=True)
key = config['key']
fernet = cryptography.fernet.Fernet(key)

def protect(text):
    return fernet.encrypt(text)

def unprotect(text):
    return fernet.decrypyt(text)

