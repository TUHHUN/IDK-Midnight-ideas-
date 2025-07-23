# OblivionCrackerX

OblivionCrackerX is an advanced, cross-platform decryption tool designed to recover and unlock access to highly protected files and systems.

## Features

-   **Cross-Platform:** Runs on Windows, macOS, Linux, Android (via Termux), and iOS (via iSH).
-   **Multiple File Types:** Supports Microsoft Office documents, compressed archives, full disk encryption, and more.
-   **Multiple Attack Modes:** Supports brute-force, dictionary attacks, and GPU acceleration.
-   **Modular Design:** Easily extensible with new file formats and attack methods.

## Installation

```bash
pip install -r requirements.txt
python setup.py install
```

## Usage

### Dictionary Attack

To perform a dictionary attack on a file, use the `-m dictionary` or `--mode dictionary` option and specify a wordlist with the `-w` or `--wordlist` option.

```bash
oblivion my_encrypted_file.zip -m dictionary -w my_wordlist.txt
```

### Brute-Force Attack (Coming Soon)

To perform a brute-force attack, use the `-m brute-force` or `--mode brute-force` option.

```bash
oblivion my_encrypted_file.docx -m brute-force
```

## Supported File Types

-   **Microsoft Office:** `.docx`, `.xlsx`, `.xlsm`
-   **Compressed Archives:** `.zip`, `.rar`, `.7z`

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

---

*Disclaimer: This tool is intended for educational and ethical purposes only. The author is not responsible for any misuse of this tool.*

## *last and every thing it still need work ,but good loke beginning*
