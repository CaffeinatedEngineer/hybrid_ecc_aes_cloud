from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature, decode_dss_signature
import os
import base64

class ECCManager:
    def __init__(self, curve_type="secp256r1"):
        """Initialize ECC manager with specified curve."""
        self.curve_map = {
            "secp256r1": ec.SECP256R1(),
            "secp384r1": ec.SECP384R1(),
            "secp521r1": ec.SECP521R1()
        }
        self.curve = self.curve_map.get(curve_type, ec.SECP256R1())
        
    def generate_key_pair(self):
        """Generate ECC key pair."""
        private_key = ec.generate_private_key(self.curve)
        public_key = private_key.public_key()
        return private_key, public_key
    
    def derive_shared_key(self, private_key, peer_public_key, key_length=32):
        """Derive shared key using ECDH."""
        shared_key = private_key.exchange(ec.ECDH(), peer_public_key)
        
        # Derive AES key from shared secret
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=key_length,
            salt=None,
            info=b'cloud-workload-encryption'
        ).derive(shared_key)
        
        return derived_key
    
    def serialize_public_key(self, public_key):
        """Serialize public key for transmission."""
        return public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    
    def deserialize_public_key(self, public_key_bytes):
        """Deserialize public key from bytes."""
        return serialization.load_pem_public_key(public_key_bytes)
    
    def sign_data(self, private_key, data):
        """Sign data using ECDSA."""
        signature = private_key.sign(data, ec.ECDSA(hashes.SHA256()))
        return base64.b64encode(signature).decode('utf-8')
    
    def verify_signature(self, public_key, data, signature):
        """Verify ECDSA signature."""
        try:
            signature_bytes = base64.b64decode(signature.encode('utf-8'))
            public_key.verify(signature_bytes, data, ec.ECDSA(hashes.SHA256()))
            return True
        except Exception:
            return False
