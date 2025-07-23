import zipfile
import rarfile
import py7zr

def is_zip_encrypted(file_path):
    """Check if a zip file is encrypted."""
    try:
        with zipfile.ZipFile(file_path) as zf:
            for zinfo in zf.infolist():
                if zinfo.flag_bits & 0x1:
                    return True
        return False
    except Exception as e:
        print(f"Error checking zip file: {e}")
        return False

def is_rar_encrypted(file_path):
    """Check if a rar file is encrypted."""
    try:
        with rarfile.RarFile(file_path) as rf:
            if rf.needs_password():
                return True
        return False
    except Exception as e:
        print(f"Error checking rar file: {e}")
        return False

def is_7z_encrypted(file_path):
    """Check if a 7z file is encrypted."""
    try:
        with py7zr.SevenZipFile(file_path, 'r') as szf:
            return szf.needs_password()
    except Exception as e:
        print(f"Error checking 7z file: {e}")
        return False

def is_archive_encrypted(file_path):
    """Check if an archive file is encrypted."""
    if file_path.endswith('.zip'):
        return is_zip_encrypted(file_path)
    elif file_path.endswith('.rar'):
        return is_rar_encrypted(file_path)
    elif file_path.endswith('.7z'):
        return is_7z_encrypted(file_path)
    return False
