# Secure Encrypt

A powerful, cross-platform, multi-layer encryption tool capable of securely encrypting any file, with features designed to confuse and mislead reverse engineers.

## Features

*   **AES-GCM Encryption**: Strong, authenticated encryption.
*   **PBKDF2 Key Derivation**: Protects against brute-force attacks.
*   **Multi-Layered Encryption**: Combines real and decoy layers to mislead attackers.
*   **Chained Keys**: Keys are linked together, requiring sequential decryption.
*   **Secure Key Storage**: Keys are stored in a JSON file, which can be optionally encrypted with a master password.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/secure-encrypt.git
    cd secure-encrypt
    ```

2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Encrypting a File

To encrypt a file, use the `encrypt` command:

```bash
python -m secure_encrypt.main encrypt /path/to/your/file.txt --layers 6 --decoys 2
```

*   `filepath`: The path to the file you want to encrypt.
*   `--layers`: (Optional) The number of real encryption layers to use (default: 6).
*   `--decoys`: (Optional) The number of decoy layers to add (default: 2).
*   `--seed`: (Optional) A seed phrase to generate the encryption keys. If you don't provide one, you'll be prompted to enter it securely.

This will create two files:

*   `file.txt.enc`: The encrypted file.
*   `keys_secure.json`: The file containing the encryption keys.

### Decrypting a File

To decrypt a file, use the `decrypt` command:

```bash
python -m secure_encrypt.main decrypt /path/to/your/file.txt.enc keys_secure.json
```

*   `filepath`: The path to the encrypted file.
*   `keys_filepath`: The path to the JSON file containing the keys.
*   `--password`: (Optional) If the keys file is encrypted, you'll be prompted to enter the master password.

This will decrypt the file and save it as `file.txt` in the same directory.

## Security Notes

*   **NEVER** lose your `keys_secure.json` file. Without it, your data is unrecoverable.
*   For maximum security, use a strong, unique seed phrase and a master password for your keys file.
*   This tool is for educational purposes. Use at your own risk.
