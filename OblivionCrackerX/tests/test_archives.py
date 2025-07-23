import unittest
from unittest.mock import patch, MagicMock
from modules.archives import is_zip_encrypted, is_rar_encrypted, is_7z_encrypted

class TestArchivesModule(unittest.TestCase):

    @patch('zipfile.ZipFile')
    def test_encrypted_zip(self, mock_zipfile):
        mock_zip = MagicMock()
        mock_zip.infolist.return_value = [MagicMock(flag_bits=0x1)]
        mock_zipfile.return_value.__enter__.return_value = mock_zip
        self.assertTrue(is_zip_encrypted('fake_encrypted.zip'))

    @patch('zipfile.ZipFile')
    def test_unencrypted_zip(self, mock_zipfile):
        mock_zip = MagicMock()
        mock_zip.infolist.return_value = [MagicMock(flag_bits=0x0)]
        mock_zipfile.return_value.__enter__.return_value = mock_zip
        self.assertFalse(is_zip_encrypted('fake_unencrypted.zip'))

    @patch('rarfile.RarFile')
    def test_encrypted_rar(self, mock_rarfile):
        mock_rar = MagicMock()
        mock_rar.needs_password.return_value = True
        mock_rarfile.return_value.__enter__.return_value = mock_rar
        self.assertTrue(is_rar_encrypted('fake_encrypted.rar'))

    @patch('rarfile.RarFile')
    def test_unencrypted_rar(self, mock_rarfile):
        mock_rar = MagicMock()
        mock_rar.needs_password.return_value = False
        mock_rarfile.return_value.__enter__.return_value = mock_rar
        self.assertFalse(is_rar_encrypted('fake_unencrypted.rar'))

    @patch('py7zr.SevenZipFile')
    def test_encrypted_7z(self, mock_7zfile):
        mock_7z = MagicMock()
        mock_7z.needs_password.return_value = True
        mock_7zfile.return_value.__enter__.return_value = mock_7z
        self.assertTrue(is_7z_encrypted('fake_encrypted.7z'))

    @patch('py7zr.SevenZipFile')
    def test_unencrypted_7z(self, mock_7zfile):
        mock_7z = MagicMock()
        mock_7z.needs_password.return_value = False
        mock_7zfile.return_value.__enter__.return_value = mock_7z
        self.assertFalse(is_7z_encrypted('fake_unencrypted.7z'))

if __name__ == '__main__':
    unittest.main()
