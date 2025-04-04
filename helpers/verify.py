from cryptography.hazmat.primitives.asymmetric import ec, ed25519
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

from helpers.file_hasher import compute_file_hash
from helpers.keyloaders import load_public_key_from_file

# ✅ Verification Function (Files)
def verify_file_signature(public_key_path, file_path: str, signature_file_path: bytes) -> bool:
    """
    Verify the signature of a file using its public key.
    Returns True if valid, False otherwise.
    """

    public_key = load_public_key_from_file(public_key_path)
    file_hash = compute_file_hash(file_path)  # Get hash of the file
    signature = signature_file_to_bytes(signature_file_path)

    try:
        if isinstance(public_key, ed25519.Ed25519PublicKey):
            public_key.verify(signature, file_hash)  # Ed25519 direct verification
        elif isinstance(public_key, ec.EllipticCurvePublicKey):
            public_key.verify(signature, file_hash, ec.ECDSA(hashes.SHA256()))  # ECDSA verification
        else:
            # return False
            raise ValueError("Unsupported key type")
        return True
    except InvalidSignature:
        return False
    
def signature_file_to_bytes(file_path: str) -> bytes:
    with open(file_path, "rb") as f:
        return f.read()