import datetime
from secure_encrypt.src.core import encrypt, derive_key, SALT_SIZE
import os

LOG_FILE = "secure_encrypt.log.enc"
LOG_KEY = "a_very_secret_key" # This should be handled more securely

def log_operation(operation: str, filepath: str, success: bool):
    """Logs an encryption or decryption operation."""

    timestamp = datetime.datetime.now().isoformat()
    log_message = f"[{timestamp}] Operation: {operation}, File: {filepath}, Success: {success}\n"

    # Encrypt the log message
    salt = os.urandom(SALT_SIZE)
    key = derive_key(LOG_KEY, salt)
    encrypted_log = encrypt(log_message.encode(), key)

    with open(LOG_FILE, 'ab') as f:
        f.write(salt + encrypted_log)
