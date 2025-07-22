import tkinter as tk
from tkinter import filedialog, messagebox
from secure_encrypt.src.file_handler import encrypt_file, decrypt_file

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Secure Encrypt")
        self.geometry("400x300")

        self.filepath = None

        # Create widgets
        self.label = tk.Label(self, text="Select a file to encrypt or decrypt.")
        self.select_button = tk.Button(self, text="Select File", command=self.select_file)
        self.encrypt_button = tk.Button(self, text="Encrypt", command=self.encrypt)
        self.decrypt_button = tk.Button(self, text="Decrypt", command=self.decrypt)

        # Layout widgets
        self.label.pack(pady=10)
        self.select_button.pack(pady=5)
        self.encrypt_button.pack(pady=5)
        self.decrypt_button.pack(pady=5)

    def select_file(self):
        self.filepath = filedialog.askopenfilename()
        if self.filepath:
            self.label.config(text=f"Selected: {self.filepath}")

    def encrypt(self):
        if not self.filepath:
            messagebox.showerror("Error", "Please select a file first.")
            return

        seed = self.prompt_for_input("Enter a seed phrase:")
        if seed:
            # For the GUI, we'll keep it simple and use a mix of algorithms
            algorithms = ['aes', 'chacha20'] * 3
            encrypt_file(self.filepath, seed, 6, 2, algorithms)
            messagebox.showinfo("Success", "File encrypted successfully.")

    def decrypt(self):
        if not self.filepath:
            messagebox.showerror("Error", "Please select a file first.")
            return

        keys_filepath = filedialog.askopenfilename(title="Select Keys File")
        if keys_filepath:
            password = self.prompt_for_input("Enter master password (if any):", show='*')
            decrypt_file(self.filepath, keys_filepath, password)
            messagebox.showinfo("Success", "File decrypted successfully.")

    def prompt_for_input(self, prompt, show=None):
        dialog = tk.Toplevel(self)
        dialog.title("Input")
        dialog.geometry("300x100")

        label = tk.Label(dialog, text=prompt)
        label.pack(pady=5)

        entry = tk.Entry(dialog, show=show)
        entry.pack(pady=5)

        result = None
        def on_ok():
            nonlocal result
            result = entry.get()
            dialog.destroy()

        ok_button = tk.Button(dialog, text="OK", command=on_ok)
        ok_button.pack(pady=5)

        self.wait_window(dialog)
        return result

if __name__ == '__main__':
    app = App()
    app.mainloop()
