from cryptography.fernet import Fernet

import os
from dotenv import load_dotenv

load_dotenv()
secure_key = os.getenv("SECRET_KEY")

# Generate 32 bytes of random data


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
        print("inside", encoded_message)
        return decrypted_msg.decode()
