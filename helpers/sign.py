from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, ed25519

from helpers.file_hasher import compute_file_hash
from helpers.keyloaders import load_private_key_from_file

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
    
def save_signature_to_file(signature: bytes, original_file_path: str):
    signature_file_path = original_file_path + ".sig"    
    try:
        with open(signature_file_path, "wb") as sig_file:
            sig_file.write(signature)
    except Exception as e:
        return None
    return (f"Signature saved to: {signature_file_path}")