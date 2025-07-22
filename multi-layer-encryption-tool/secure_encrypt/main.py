import argparse
import sys
from getpass import getpass
from secure_encrypt.src.file_handler import encrypt_file, decrypt_file
from secure_encrypt.src.gui import App

def main():
    parser = argparse.ArgumentParser(description="A multi-layer encryption tool.")
    parser.add_argument('--gui', action='store_true', help='Launch the graphical user interface.')

    # Keep the subparsers for the CLI
    subparsers = parser.add_subparsers(dest='command')

    # Encrypt command
    encrypt_parser = subparsers.add_parser('encrypt', help='Encrypt a file.')
    encrypt_parser.add_argument('filepath', type=str, help='The path to the file to encrypt.')
    encrypt_parser.add_argument('--layers', type=int, default=6, help='Number of real encryption layers.')
    encrypt_parser.add_argument('--decoys', type=int, default=2, help='Number of decoy layers.')
    encrypt_parser.add_argument('--seed', type=str, help='A seed phrase to generate keys. If not provided, will be prompted.')
    encrypt_parser.add_argument('--algorithms', nargs='+', default=['aes'], help='A list of algorithms to use for each layer (e.g., aes chacha20).')
    encrypt_parser.add_argument('--obfuscate', nargs='+', type=int, default=[], help='A list of layer indices to obfuscate (e.g., 0 2 4).')
    encrypt_parser.add_argument('--output-dir', type=str, default='.', help='The directory to save the encrypted file and keys.')
    encrypt_parser.add_argument('--qr-code', type=str, help='The path to save a QR code of the keys.')

    # Decrypt command
    decrypt_parser = subparsers.add_parser('decrypt', help='Decrypt a file.')
    decrypt_parser.add_argument('filepath', type=str, help='The path to the file to decrypt.')
    decrypt_parser.add_argument('keys_filepath', type=str, help='The path to the keys file.')
    decrypt_parser.add_argument('--password', type=str, help='Master password for the keys file. If not provided, will be prompted.')
    decrypt_parser.add_argument('--verify-integrity', action='store_true', help='Verify the integrity of the file before decryption.')
    decrypt_parser.add_argument('--self-destruct-on-failure', type=int, default=0, help='The number of failed decryption attempts before the file is deleted.')

    args = parser.parse_args()

    if args.gui:
        app = App()
        app.mainloop()
        sys.exit()

    if args.command == 'encrypt':
        seed = args.seed or getpass("Enter a seed phrase to generate keys: ")

        # Ensure the number of algorithms matches the number of layers
        if len(args.algorithms) != args.layers:
            # If only one algorithm is provided, use it for all layers
            if len(args.algorithms) == 1:
                args.algorithms = args.algorithms * args.layers
            else:
                print("Error: The number of algorithms must match the number of layers.")
                sys.exit(1)

        obfuscate_layers = [i in args.obfuscate for i in range(args.layers)]

        encrypt_file(args.filepath, seed, args.layers, args.decoys, args.algorithms, args.output_dir, obfuscate_layers)

        if args.qr_code:
            from secure_encrypt.src.key_manager import generate_key_chain, generate_qr_code_for_keys
            keys = generate_key_chain(seed, args.layers)
            generate_qr_code_for_keys(keys, args.qr_code)
            print(f"QR code saved to {args.qr_code}")

    elif args.command == 'decrypt':
        password = args.password or getpass("Enter the master password for the keys file (if any): ")
        decrypt_file(args.filepath, args.keys_filepath, password)

    elif not args.command:
        parser.print_help()


if __name__ == '__main__':
    main()
