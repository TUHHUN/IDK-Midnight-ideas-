from secure_encrypt.src.layers import LAYER_SEPARATOR, build_encryption_layers
from secure_encrypt.src.key_manager import generate_key_chain, save_keys_to_file, load_keys_from_file
from secure_encrypt.src.core import decrypt_aes, decrypt_chacha20, derive_key
import base64

from secure_encrypt.src.logger import log_operation

from secure_encrypt.src.core import generate_hmac

import os

def encrypt_file(filepath: str, seed: str, num_real_layers: int, num_decoy_layers: int, algorithms: list, output_dir: str = '.', obfuscate_layers: list = []):
    """Encrypts a file and saves it with the layered structure."""
    try:
        keys = generate_key_chain(seed, num_real_layers)

        os.makedirs(output_dir, exist_ok=True)

        keys_filepath = os.path.join(output_dir, 'keys_secure.json')
        save_keys_to_file(keys, keys_filepath)

        with open(filepath, 'rb') as f:
            data = f.read()

        layers = build_encryption_layers(data, keys, num_real_layers, num_decoy_layers, algorithms, obfuscate_layers)

        encrypted_content = LAYER_SEPARATOR.join(layers)

        hmac_key = keys[-1]
        hmac = generate_hmac(encrypted_content, hmac_key)

        encrypted_filename = os.path.basename(filepath) + '.enc'
        encrypted_filepath = os.path.join(output_dir, encrypted_filename)

        with open(encrypted_filepath, 'wb') as f:
            f.write(b"SECURE_ENCRYPT_V1.0" + LAYER_SEPARATOR)
            f.write(encrypted_content)
            f.write(LAYER_SEPARATOR)
            f.write(hmac)

        print(f"File encrypted successfully: {encrypted_filepath}")
        log_operation('encrypt', filepath, True)
    except Exception as e:
        print(f"Encryption failed: {e}")
        log_operation('encrypt', filepath, False)

from secure_encrypt.src.core import verify_hmac

def decrypt_file(encrypted_filepath: str, keys_filepath: str, master_password: str = None, verify_integrity: bool = True, self_destruct_attempts: int = 0):
    """Decrypts a file with a layered structure."""
    try:
        if self_destruct_attempts > 0:
            failure_count = 0

        keys = load_keys_from_file(keys_filepath, master_password)

        with open(encrypted_filepath, 'rb') as f:
            content = f.read()

        parts = content.split(LAYER_SEPARATOR)
        watermark = parts[0]

        if watermark != b"SECURE_ENCRYPT_V1.0":
            print("Warning: Watermark not found or is incorrect.")

        encrypted_content = LAYER_SEPARATOR.join(parts[1:-1])
        hmac_from_file = parts[-1]

        hmac_key = keys[-1]
        if verify_integrity and not verify_hmac(encrypted_content, hmac_key, hmac_from_file):
            print("Error: HMAC verification failed.")
            if self_destruct_attempts > 0:
                failure_count += 1
                if failure_count >= self_destruct_attempts:
                    os.remove(encrypted_filepath)
                    print("Self-destruct sequence initiated.")
            log_operation('decrypt', encrypted_filepath, False)
            return

        layers = encrypted_content.split(LAYER_SEPARATOR)

        current_key = keys[0]
        decrypted_data = None

        for i in range(len(keys)):
            for layer in layers:
                salt = layer[:16]
                encrypted_data = layer[16:]

                derived_key = derive_key(base64.b64encode(current_key).decode(), salt)

                # Try decrypting with and without unshuffling
                for unshuffled_data in [unshuffle_bytes(encrypted_data, current_key), encrypted_data]:
                    for decrypt_func in [decrypt_aes, decrypt_chacha20]:
                        decrypted_layer = decrypt_func(unshuffled_data, derived_key)

                        if decrypted_layer:
                            try:
                                parts = decrypted_layer.split(b'||')
                                algorithm = parts[0].decode()
                                next_key_b64 = parts[1]
                                data = b'||'.join(parts[2:])

                                next_key = base64.b64decode(next_key_b64)

                                if next_key == keys[i+1]:
                                     current_key = next_key
                                     decrypted_data = data
                                     print(f"Successfully decrypted a layer with {algorithm}.")
                                     break
                                elif next_key == b'final' and i == len(keys) - 1:
                                    decrypted_data = data
                                    print(f"Successfully decrypted the final layer with {algorithm}.")
                                    break

                            except Exception:
                                continue
                        if decrypted_data:
                            break
                    if decrypted_data:
                        break
                if decrypted_data and (next_key == keys[i+1] or next_key == b'final'):
                    break
            if next_key == b'final':
                break

        if not decrypted_data:
            print("Decryption failed.")
            if self_destruct_attempts > 0:
                failure_count += 1
                if failure_count >= self_destruct_attempts:
                    os.remove(encrypted_filepath)
                    print("Self-destruct sequence initiated.")
            log_operation('decrypt', encrypted_filepath, False)
        else:
            original_filepath = encrypted_filepath.replace('.enc', '')
            with open(original_filepath, 'wb') as f:
                f.write(decrypted_data)
            print(f"File decrypted successfully: {original_filepath}")
            log_operation('decrypt', encrypted_filepath, True)
    except Exception as e:
        print(f"Decryption failed: {e}")
        log_operation('decrypt', encrypted_filepath, False)
