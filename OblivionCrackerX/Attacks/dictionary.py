def dictionary_attack(file_path, wordlist_path, decrypt_func):
    """
    Performs a dictionary attack on a file.

    Args:
        file_path (str): The path to the encrypted file.
        wordlist_path (str): The path to the wordlist.
        decrypt_func (function): The function to call to attempt decryption.
                                 This function should take the file path and a
                                 password as arguments and return True if
                                 decryption is successful, False otherwise.
    """
    with open(wordlist_path, 'r', encoding='latin-1') as f:
        for password in f:
            password = password.strip()
            print(f"[*] Trying password: {password}")
            if decrypt_func(file_path, password):
                print(f"[+] Password found: {password}")
                return password
    print("[-] Password not found in wordlist.")
    return None
