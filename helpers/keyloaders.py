from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

def load_private_key_from_file(file_path: str, passphrase: str = None):
    with open(file_path, "rb") as f:
        pem_data = f.read()
    
    # Convert passphrase to bytes if provided
    password_bytes = passphrase.encode() if passphrase else None

    try:
        private_key = serialization.load_pem_private_key(
            pem_data,
            password=password_bytes,
            backend=default_backend()
        )
        return private_key
    except ValueError as e:
        raise ValueError(f"Failed to load private key: {e}")
    
def load_public_key_from_file(file_path: str):
    with open(file_path, "rb") as f:
        pem_data = f.read()

    try:
        public_key = serialization.load_pem_public_key(
            pem_data,
            backend=default_backend()
        )
        return public_key
    except ValueError as e:
        raise ValueError(f"Failed to load public key: {e}")