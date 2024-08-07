from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()
secure_key = os.getenv("SECRET_KEY")

# Generate a new key if SECRET_KEY is not set
if not secure_key:
    secure_key = Fernet.generate_key().decode()
    print(f"Generated new key: {secure_key}")
    # Store this key securely, e.g., in your .env file
    # Remember to add SECRET_KEY=<generated_key> to your .env file

# Create a Fernet object with the secure key
f = Fernet(secure_key.encode())

def encrypt_message(message):
    if message and message.strip():
        # Encode the message as bytes before encryption
        message_bytes = message.encode()
        # Encrypt the message using the Fernet object
        encrypted_msg = f.encrypt(message_bytes)
        return encrypted_msg
    return None

def decrypt_message(encoded_message):
    if encoded_message:
        decrypted_msg = f.decrypt(encoded_message)
        return decrypted_msg.decode()

# Example usage
if __name__ == "__main__":
    original_message = "Hello, World!"
    print(f"Original Message: {original_message}")

    encrypted_message = encrypt_message(original_message)
    print(f"Encrypted Message: {encrypted_message}")

    decrypted_message = decrypt_message(encrypted_message)
    print(f"Decrypted Message: {decrypted_message}")

    assert original_message == decrypted_message, "Decryption failed!"
