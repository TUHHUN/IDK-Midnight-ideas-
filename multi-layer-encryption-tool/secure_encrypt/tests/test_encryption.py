import os
import unittest
from secure_encrypt.src.file_handler import encrypt_file, decrypt_file

class TestEncryption(unittest.TestCase):

    def test_encrypt_decrypt_cycle(self):
        # Create a dummy file to encrypt
        with open('test_file.txt', 'w') as f:
            f.write('This is a test file for the encryption tool.')

        # Encrypt the file
        encrypt_file('test_file.txt', 'test_seed', 2, 1)

        # Decrypt the file
        decrypt_file('test_file.txt.enc', 'keys_secure.json')

        # Check if the decrypted file matches the original
        with open('test_file.txt', 'r') as f:
            decrypted_content = f.read()

        # Re-read original content to be safe
        with open('test_file.txt', 'r') as f:
            original_content = f.read()

        self.assertEqual(decrypted_content, original_content)

        # Clean up the created files
        os.remove('test_file.txt')
        os.remove('test_file.txt.enc')
        os.remove('keys_secure.json')

if __name__ == '__main__':
    unittest.main()
