import unittest
from unittest.mock import patch, MagicMock
from modules.office import is_office_encrypted

class TestOfficeModule(unittest.TestCase):

    @patch('olefile.isOleFile')
    @patch('olefile.OleFileIO')
    def test_encrypted_file(self, mock_olefile_io, mock_is_ole_file):
        mock_is_ole_file.return_value = True
        mock_ole = MagicMock()
        mock_ole.exists.return_value = True
        mock_olefile_io.return_value = mock_ole

        self.assertTrue(is_office_encrypted('fake_encrypted.docx'))

    @patch('olefile.isOleFile')
    @patch('olefile.OleFileIO')
    def test_unencrypted_file(self, mock_olefile_io, mock_is_ole_file):
        mock_is_ole_file.return_value = True
        mock_ole = MagicMock()
        mock_ole.exists.return_value = False
        mock_olefile_io.return_value = mock_ole

        self.assertFalse(is_office_encrypted('fake_unencrypted.docx'))

    @patch('olefile.isOleFile')
    def test_not_ole_file(self, mock_is_ole_file):
        mock_is_ole_file.return_value = False
        self.assertFalse(is_office_encrypted('not_an_ole_file.txt'))

if __name__ == '__main__':
    unittest.main()
# @CVBlq
