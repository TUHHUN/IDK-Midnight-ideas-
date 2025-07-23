import argparse

def main():
    parser = argparse.ArgumentParser(description="OblivionCrackerX: Advanced, Cross-Platform Decryption Tool")
    parser.add_argument("file", help="Path to the encrypted file")
    parser.add_argument("-m", "--mode", choices=["brute-force", "dictionary"], default="dictionary", help="Attack mode")
    parser.add_argument("-w", "--wordlist", help="Path to the wordlist for dictionary attack")
    parser.add_argument("--gpu", action="store_true", help="Enable GPU acceleration with hashcat")

    args = parser.parse_args()

    print(f"[*] Target File: {args.file}")
    print(f"[*] Attack Mode: {args.mode}")

    if args.mode == "dictionary" and not args.wordlist:
        parser.error("--wordlist is required for dictionary attack mode")

    # Placeholder for main logic
    print("[*] Commencing decryption...")

    file_type = detect_file_type(args.file)

    if file_type == "office":
        if is_office_encrypted(args.file):
            print("[+] Office file is encrypted. Ready to proceed with decryption.")
            if args.mode == "dictionary":
                password = dictionary_attack(args.file, args.wordlist, decrypt_office)
                if password:
                    print(f"[+] Decryption successful. Password is: {password}")
                else:
                    print("[-] Decryption failed.")
        else:
            print("[-] Office file is not encrypted.")
            return
    elif file_type == "archive":
        if is_archive_encrypted(args.file):
            print("[+] Archive file is encrypted. Ready to proceed with decryption.")
            if args.mode == "dictionary":
                password = dictionary_attack(args.file, args.wordlist, decrypt_archive)
                if password:
                    print(f"[+] Decryption successful. Password is: {password}")
                else:
                    print("[-] Decryption failed.")
        else:
            print("[-] Archive file is not encrypted.")
            return
    elif file_type == "unknown":
        print(f"[-] Unknown or unsupported file type: {args.file}")
        return

def decrypt_office(file_path, password):
    # Placeholder for office decryption logic
    return False

def decrypt_archive(file_path, password):
    # Placeholder for archive decryption logic
    return False

if __name__ == "__main__":
    from utils.file_detector import detect_file_type
    from modules.office import is_office_encrypted
    from modules.archives import is_archive_encrypted
    from attacks.dictionary import dictionary_attack
    main()
