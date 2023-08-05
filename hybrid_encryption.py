from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
import os
import glob

# Fixed Initialization Vector (IV)
IV = b"ThisIsARandomIV!"

def encrypt_file(file_path, public_key):
    with open(file_path, "rb") as file:
        file_data = file.read()

    # Generate a random 128-bit key
    aes_key = os.urandom(16)

    # Encrypt the file using AES-CBC with the key
    cipher = AES.new(aes_key, AES.MODE_CBC)
    encrypted_data = cipher.encrypt(file_data)

    # Save the encrypted file with the same name but in the encrypted_files folder
    encrypted_filename = os.path.join("encrypted_files", os.path.basename(file_path))
    with open(encrypted_filename, "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)

    # Encrypt the AES key with the RSA public key
    rsa_cipher = PKCS1_OAEP.new(public_key)
    encrypted_aes_key = rsa_cipher.encrypt(aes_key)

    # Store the encrypted AES key with the same name as the file but with a ".key" extension
    key_filename = os.path.join("encrypted_files", os.path.basename(file_path) + ".key")
    with open(key_filename, "wb") as key_file:
        key_file.write(encrypted_aes_key)

def decrypt_file(encrypted_file, key_file, private_key):
    with open(encrypted_file, "rb") as file:
        encrypted_data = file.read()
    with open(key_file, "rb") as key:
        encrypted_aes_key = key.read()

    # Decrypt the AES key using the RSA private key
    rsa_cipher = PKCS1_OAEP.new(private_key)
    aes_key = rsa_cipher.decrypt(encrypted_aes_key)

    # Decrypt the file using AES-CBC with the decrypted key
    cipher = AES.new(aes_key, AES.MODE_CBC)
    decrypted_data = cipher.decrypt(encrypted_data)

    # Save the decrypted data to a new file with the "_decrypted" suffix
    decrypted_filename = os.path.join("decrypted_files", os.path.basename(encrypted_file) + "_decrypted.txt")
    with open(decrypted_filename, "wb") as decrypted_file:
        decrypted_file.write(decrypted_data)

def main():
    # Load the RSA keys from the key files
    with open("public_key_1.pem", "rb") as f:
        public_key_1 = RSA.import_key(f.read())
    with open("private_key_1.pem", "rb") as f:
        private_key_1 = RSA.import_key(f.read())

    with open("public_key_2.pem", "rb") as f:
        public_key_2 = RSA.import_key(f.read())
    with open("private_key_2.pem", "rb") as f:
        private_key_2 = RSA.import_key(f.read())

    # Create a folder to store encrypted files
    if not os.path.exists("encrypted_files"):
        os.makedirs("encrypted_files")

    # Get the list of text files in the current folder
    files = glob.glob("*.txt")

    for file in files:
        if "file1" in file:  # Encrypt with the first key pair
            encrypt_file(file, public_key_1)
        elif "file2" in file:  # Encrypt with the second key pair
            encrypt_file(file, public_key_2)

    # Create a folder to store decrypted files
    if not os.path.exists("decrypted_files"):
        os.makedirs("decrypted_files")

    # Decrypt the encrypted files
    encrypted_files = glob.glob("encrypted_files/*.txt")
    key_files = glob.glob("encrypted_files/*.key")
    for encrypted_file, key_file in zip(encrypted_files, key_files):
        if "file1" in encrypted_file:  # Decrypt using the first private key
            decrypt_file(encrypted_file, key_file, private_key_1)
        elif "file2" in encrypted_file:  # Decrypt using the second private key
            decrypt_file(encrypted_file, key_file, private_key_2)

if __name__ == "__main__":
    main()