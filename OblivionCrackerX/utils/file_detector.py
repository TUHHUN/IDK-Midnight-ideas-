import os

def detect_file_type(file_path):
    """
    Detects the file type based on the file extension.
    """
    _, extension = os.path.splitext(file_path)
    extension = extension.lower()

    if extension in [".docx", ".xlsx", ".xlsm"]:
        return "office"
    elif extension in [".zip", ".rar", ".7z"]:
        return "archive"
    elif extension in [".bitlocker", ".truecrypt", ".veracrypt"]:
        return "disk"
    elif extension in [".sam", ".system"]:
        return "os_creds"
    elif "keychain" in file_path.lower():
        return "os_creds"
    elif "manifest.db" in file_path.lower():
        return "ios"
    else:
        return "unknown"
