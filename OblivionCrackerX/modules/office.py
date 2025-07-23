import olefile

def is_office_encrypted(file_path):
    """
    Check if a Microsoft Office file is encrypted.
    """
    try:
        if not olefile.isOleFile(file_path):
            return False

        ole = olefile.OleFileIO(file_path)
        if ole.exists('EncryptedPackage'):
            return True
        if ole.exists('EncryptionInfo'):
             return True
        return False
    except Exception as e:
        print(f"Error checking file: {e}")
        return False
