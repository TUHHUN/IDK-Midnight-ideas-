import os
import zlib
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import pysodium

# Constants
SALT_SIZE = 16
KEY_SIZE = 32
ITERATIONS = 100000
NONCE_SIZE_AES = 12
NONCE_SIZE_CHACHA = 24

def derive_key(password: str, salt: bytes) -> bytes:
    """Derives a key from a password and salt using PBKDF2-HMAC-SHA256."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_aes(data: bytes, key: bytes) -> bytes:
    """Compresses and encrypts data using AES-GCM."""
    compressed_data = zlib.compress(data)
    nonce = os.urandom(NONCE_SIZE_AES)
    aesgcm = AESGCM(key)
    encrypted_data = aesgcm.encrypt(nonce, compressed_data, None)
    return nonce + encrypted_data

def decrypt_aes(encrypted_data: bytes, key: bytes) -> bytes:
    """Decrypts and decompresses data using AES-GCM."""
    nonce = encrypted_data[:NONCE_SIZE_AES]
    ciphertext = encrypted_data[NONCE_SIZE_AES:]
    aesgcm = AESGCM(key)
    try:
        decrypted_data = aesgcm.decrypt(nonce, ciphertext, None)
        return zlib.decompress(decrypted_data)
    except Exception as e:
        print(f"AES Decryption failed: {e}")
        return None

def encrypt_chacha20(data: bytes, key: bytes) -> bytes:
    """Compresses and encrypts data using ChaCha20-Poly1305."""
    compressed_data = zlib.compress(data)
    nonce = os.urandom(NONCE_SIZE_CHACHA)
    encrypted_data = pysodium.crypto_aead_chacha20poly1305_ietf_encrypt(compressed_data, None, nonce, key)
    return nonce + encrypted_data

def decrypt_chacha20(encrypted_data: bytes, key: bytes) -> bytes:
    """Decrypts and decompresses data using ChaCha20-Poly1305."""
    nonce = encrypted_data[:NONCE_SIZE_CHACHA]
    ciphertext = encrypted_data[NONCE_SIZE_CHACHA:]
    try:
        decrypted_data = pysodium.crypto_aead_chacha20poly1305_ietf_decrypt(ciphertext, None, nonce, key)
        return zlib.decompress(decrypted_data)
    except pysodium.exceptions.SodiumError as e:
        print(f"ChaCha20 Decryption failed: {e}")
        return None

import hmac, hashlib

def generate_hmac(data: bytes, key: bytes) -> bytes:
    """Generates an HMAC for the given data."""
    return hmac.new(key, data, hashlib.sha256).digest()

def verify_hmac(data: bytes, key: bytes, hmac_to_verify: bytes) -> bool:
    """Verifies an HMAC for the given data."""
    return hmac.compare_digest(hmac.new(key, data, hashlib.sha256).digest(), hmac_to_verify)

import random

def shuffle_bytes(data: bytes, seed: bytes) -> bytes:
    """Shuffles the bytes of a byte string based on a seed."""
    random.seed(seed)
    index = list(range(len(data)))
    random.shuffle(index)
    return bytes([data[i] for i in index])

def unshuffle_bytes(data: bytes, seed: bytes) -> bytes:
    """Unshuffles the bytes of a byte string based on a seed."""
    random.seed(seed)
    index = list(range(len(data)))
    random.shuffle(index)

    unshuffled_data = bytearray(len(data))
    for i, j in enumerate(index):
        unshuffled_data[j] = data[i]

    return bytes(unshuffled_data)

# Default encrypt and decrypt functions (can be changed)
encrypt = encrypt_aes
decrypt = decrypt_aes
