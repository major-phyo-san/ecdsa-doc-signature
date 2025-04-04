from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

def generate_keypair(curve_name = "ed25519"):
    # Dictionary to map curve names to cryptography classes
    curve_map = {
        "secp224r1": ec.SECP224R1,
        "secp256k1": ec.SECP256K1,  # Used in Bitcoin & Ethereum
        "secp256r1": ec.SECP256R1,  # General-Purpose (Web, TLS, Digital Signatures, Blockchain), (NIST P-256), Same as prime256v1
        "secp384r1": ec.SECP384R1,  # Higher Security (Government, Long-Term Security)
        "secp521r1": ec.SECP521R1,  # Ultra-Secure (Rare Use Cases, High Computational Power)
        "prime192v1": ec.SECP192R1,  # Same as secp192r1
        "prime256v1": ec.SECP256R1,  # Same as secp256r1
        "ed25519": "default",  # default
    }

    # User-defined curve name (mimicking PHP behavior)
    # curve_name = "ed25519"  # Change this to another curve if needed
    if curve_name != "ed25519":
        # Check if curve exists
        if curve_name not in curve_map:
            raise ValueError(f"Unsupported curve name: {curve_name}")
            return {}

        # Generate private key using the selected curve
        curve_class = curve_map[curve_name]()
        private_key = ec.generate_private_key(curve_class)

        # # Prompt user for passphrase
        # passphrase = getpass.getpass("Enter passphrase (leave blank for no encryption): ").encode()

        # # Set encryption method
        # if passphrase:
        #     encryption = serialization.BestAvailableEncryption(passphrase)  # AES-256-CBC encryption
        # else:
        #     encryption = serialization.NoEncryption()  # No encryption if blank

        encryption = serialization.NoEncryption()  # No encryption if blank

        # Export private key to PEM format with encryption
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,  # Standard format
            encryption_algorithm=encryption
        )

        # Extract public key
        public_key = private_key.public_key()
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    else:
        # Generate a new Ed25519 private key
        private_key = ed25519.Ed25519PrivateKey.generate()
        # Get the public key
        public_key = private_key.public_key()

        # Export the private key to PEM format
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()  # No encryption (Ed25519 doesn't support encrypted keys)
        )

        # Export the public key to PEM format
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    return {
        "public_pem":  public_pem, 
        "private_pem": private_pem
    }