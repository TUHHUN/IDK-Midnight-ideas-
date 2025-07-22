import os
import random
import base64
from secure_encrypt.src.core import encrypt_aes, encrypt_chacha20, derive_key, SALT_SIZE

LAYER_SEPARATOR = b"---LAYER_SEPARATOR---"

from secure_encrypt.src.core import shuffle_bytes, unshuffle_bytes

def create_real_layer(data: bytes, key: bytes, next_key: bytes, algorithm: str = 'aes', obfuscate: bool = False) -> bytes:
    """Creates a real encryption layer."""
    salt = os.urandom(SALT_SIZE)
    derived_key = derive_key(base64.b64encode(key).decode(), salt)

    data_with_next_key = f"{algorithm}||".encode() + base64.b64encode(next_key) + b'||' + data

    if algorithm == 'aes':
        encrypted_data = encrypt_aes(data_with_next_key, derived_key)
    elif algorithm == 'chacha20':
        encrypted_data = encrypt_chacha20(data_with_next_key, derived_key)
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

    if obfuscate:
        encrypted_data = shuffle_bytes(encrypted_data, key)

    return salt + encrypted_data

def create_decoy_layer() -> bytes:
    """Creates a decoy encryption layer with random data and a random key."""
    decoy_data = os.urandom(random.randint(128, 1024))
    decoy_key = os.urandom(32)
    salt = os.urandom(SALT_SIZE)
    derived_key = derive_key(base64.b64encode(decoy_key).decode(), salt)

    # Use a random algorithm for the decoy layer
    if random.choice([True, False]):
        encrypted_data = encrypt_aes(decoy_data, derived_key)
    else:
        encrypted_data = encrypt_chacha20(decoy_data, derived_key)

    return salt + encrypted_data

def build_encryption_layers(data: bytes, keys: list, num_real_layers: int, num_decoy_layers: int, algorithms: list, obfuscate_layers: list) -> list:
    """Builds and shuffles real and decoy encryption layers."""
    layers = []

    for i in range(num_real_layers):
        key = keys[i]
        next_key = keys[i+1] if i + 1 < len(keys) else b'final'
        algorithm = algorithms[i]
        obfuscate = obfuscate_layers[i]

        if i == 0:
            layer_data = data
        else:
            layer_data = layers[-1]

        layers.append(create_real_layer(layer_data, key, next_key, algorithm, obfuscate))

    for _ in range(num_decoy_layers):
        layers.append(create_decoy_layer())

    random.shuffle(layers)
    return layers
