import os
import json
import base64
import hashlib
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Constants
KEY_SIZE = 32
SALT_SIZE = 16
ITERATIONS = 100000

def generate_initial_key(seed: str) -> bytes:
    """Generates the initial key from a seed."""
    salt = os.urandom(SALT_SIZE)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend()
    )
    return kdf.derive(seed.encode())

def generate_chained_key(previous_key: bytes) -> bytes:
    """Generates a chained key based on the previous key."""
    # New salt for each key derivation
    salt = os.urandom(SALT_SIZE)

    # Derive the new key using the previous key and a new salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend()
    )

    # The new key is a combination of a hash of the previous key and a new derived key
    hashed_prev_key = hashlib.sha256(previous_key).digest()
    derived_part = kdf.derive(previous_key)

    # Combine them to form the new key
    new_key = hashed_prev_key[:16] + derived_part[:16]
    return new_key

def generate_key_chain(seed: str, num_keys: int) -> list:
    """Generates a chain of keys."""
    keys = []
    initial_key = generate_initial_key(seed)
    keys.append(initial_key)

    current_key = initial_key
    for _ in range(num_keys - 1):
        next_key = generate_chained_key(current_key)
        keys.append(next_key)
        current_key = next_key

    return keys

from secure_encrypt.src.core import encrypt, decrypt, derive_key

def save_keys_to_file(keys: list, filepath: str, master_password: str = None):
    """Saves keys to a JSON file, optionally encrypted."""
    keys_b64 = [base64.urlsafe_b64encode(key).decode('utf-8') for key in keys]

    data_to_save = json.dumps(keys_b64, indent=4).encode()

    if master_password:
        salt = os.urandom(SALT_SIZE)
        key = derive_key(master_password, salt)
        encrypted_data = encrypt(data_to_save, key)
        with open(filepath, 'wb') as f:
            f.write(salt + encrypted_data)
    else:
        with open(filepath, 'w') as f:
            f.write(data_to_save.decode())

import qrcode

def generate_qr_code_for_keys(keys: list, filepath: str):
    """Generates a QR code containing the keys."""
    keys_b64 = [base64.urlsafe_b64encode(key).decode('utf-8') for key in keys]
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(json.dumps(keys_b64))
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filepath)

def load_keys_from_file(filepath: str, master_password: str = None) -> list:
    """Loads keys from a JSON file, optionally decrypted."""
    if master_password:
        with open(filepath, 'rb') as f:
            data = f.read()
        salt = data[:SALT_SIZE]
        encrypted_data = data[SALT_SIZE:]
        key = derive_key(master_password, salt)
        decrypted_data = decrypt(encrypted_data, key)
        keys_b64 = json.loads(decrypted_data)
    else:
        with open(filepath, 'r') as f:
            keys_b64 = json.load(f)

    keys = [base64.urlsafe_b64decode(key) for key in keys_b64]
    return keys
