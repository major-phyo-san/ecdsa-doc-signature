from cryptography.hazmat.primitives import hashes

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