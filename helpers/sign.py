from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, ed25519

# 📄 Function to Compute File Hash (SHA-256)
def compute_file_hash(file_path: str) -> bytes:
    """
    Compute SHA-256 hash of a file.
    This ensures we sign only a small fixed-size hash instead of large files.
    """
    digest = hashes.Hash(hashes.SHA256())
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):  # Read in chunks to handle large files
            digest.update(chunk)
    return digest.finalize()

# 🔏 Signing Function (Files)
def sign_file(private_key_path: str, file_path: str) -> bytes:
    """
    Sign a file using either ECDSA or Ed25519 private key.
    Returns the signature.
    """
    private_key = load_private_key_from_file(private_key_path)
    file_hash = compute_file_hash(file_path)  # Get hash of the file
    if isinstance(private_key, ed25519.Ed25519PrivateKey):
        return private_key.sign(file_hash)  # Ed25519 signs raw hash
    elif isinstance(private_key, ec.EllipticCurvePrivateKey):
        return private_key.sign(file_hash, ec.ECDSA(hashes.SHA256()))  # ECDSA uses hashing
    else:
        raise ValueError("Unsupported key type")
    
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
    
def save_signature_to_file(signature: bytes, original_file_path: str):
    signature_file_path = original_file_path + ".sig"    
    try:
        with open(signature_file_path, "wb") as sig_file:
            sig_file.write(signature)
    except Exception as e:
        return None
    return (f"Signature saved to: {signature_file_path}")