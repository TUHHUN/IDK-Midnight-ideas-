import unittest
from unittest.mock import mock_open, patch
from attacks.dictionary import dictionary_attack

class TestDictionaryAttack(unittest.TestCase):

    def test_password_found(self):
        m = mock_open(read_data="password\n123456\nqwerty")
        with patch('builtins.open', m):
            decrypt_func = lambda file_path, password: password == "123456"
            result = dictionary_attack("fake_file.zip", "dummy_wordlist.txt", decrypt_func)
            self.assertEqual(result, "123456")

    def test_password_not_found(self):
        m = mock_open(read_data="password\n123456\nqwerty")
        with patch('builtins.open', m):
            decrypt_func = lambda file_path, password: password == "admin"
            result = dictionary_attack("fake_file.zip", "dummy_wordlist.txt", decrypt_func)
            self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
