"""Cryptography utilities."""
import hashlib
import hmac
import base64
from cryptography.fernet import Fernet
import os

# AES key for encrypting WDT appsecret (must be 32 bytes, base64 encoded)
WDT_CRYPTO_KEY = os.environ.get("WDT_CRYPTO_KEY", Fernet.generate_key().decode())


def encrypt_aes256(plaintext: str, key: str = WDT_CRYPTO_KEY) -> str:
    """Encrypt plaintext using AES-256 (Fernet)."""
    f = Fernet(key.encode() if isinstance(key, str) else key)
    return f.encrypt(plaintext.encode()).decode()


def decrypt_aes256(ciphertext: str, key: str = WDT_CRYPTO_KEY) -> str:
    """Decrypt ciphertext using AES-256 (Fernet)."""
    f = Fernet(key.encode() if isinstance(key, str) else key)
    return f.decrypt(ciphertext.encode()).decode()
