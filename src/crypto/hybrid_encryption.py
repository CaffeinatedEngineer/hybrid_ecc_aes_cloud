import json
import time
from .ecc_manager import ECCManager
from .aes_manager import AESManager

class HybridECCAES:
    def __init__(self, ecc_curve="secp256r1", aes_key_size=256):
        """Initialize hybrid ECC-AES encryption system."""
        self.ecc_manager = ECCManager(ecc_curve)
        self.aes_manager = AESManager(aes_key_size)
        
        # Generate server key pair (in practice, this would be stored securely)
        self.server_private_key, self.server_public_key = self.ecc_manager.generate_key_pair()
    
    def encrypt_workload(self, workload_data, cloud_region="us-east-1", workload_type="compute"):
        """
        Encrypt cloud workload data using hybrid ECC-AES.
        
        NOVELTY: 
        1. Cloud-specific key derivation based on region and workload type
        2. ECC replaces RSA for better performance
        3. Workload metadata integration for access control
        """
        start_time = time.time()
        
        # Step 1: Generate ephemeral ECC key pair for this workload
        client_private_key, client_public_key = self.ecc_manager.generate_key_pair()
        
        # Step 2: Derive shared secret using ECDH
        shared_secret = self.ecc_manager.derive_shared_key(
            client_private_key, 
            self.server_public_key
        )
        
        # Step 3: Generate AES key from shared secret + cloud metadata
        # NOVELTY: Include cloud region and workload type in key derivation
        metadata = f"{cloud_region}:{workload_type}".encode('utf-8')
        aes_key = self._derive_cloud_specific_key(shared_secret, metadata)
        
        # Step 4: Encrypt workload data with AES
        encrypted_data = self.aes_manager.encrypt_data(workload_data, aes_key)
        
        # Step 5: Create workload package with metadata
        workload_package = {
            "encrypted_data": encrypted_data,
            "client_public_key": self.ecc_manager.serialize_public_key(client_public_key).decode('utf-8'),
            "cloud_region": cloud_region,
            "workload_type": workload_type,
            "timestamp": time.time(),
            "encryption_time": time.time() - start_time
        }
        
        # Step 6: Sign the package for integrity
        package_json = json.dumps(workload_package, sort_keys=True)
        signature = self.ecc_manager.sign_data(self.server_private_key, package_json.encode('utf-8'))
        workload_package["signature"] = signature
        
        return workload_package
    
    def decrypt_workload(self, workload_package):
        """Decrypt cloud workload data."""
        start_time = time.time()
        
        # Step 1: Verify package integrity
        package_copy = workload_package.copy()
        signature = package_copy.pop("signature")
        package_json = json.dumps(package_copy, sort_keys=True)
        
        if not self.ecc_manager.verify_signature(
            self.server_public_key, 
            package_json.encode('utf-8'), 
            signature
        ):
            raise ValueError("Workload package signature verification failed")
        
        # Step 2: Deserialize client public key
        client_public_key = self.ecc_manager.deserialize_public_key(
            workload_package["client_public_key"].encode('utf-8')
        )
        
        # Step 3: Derive shared secret
        shared_secret = self.ecc_manager.derive_shared_key(
            self.server_private_key,
            client_public_key
        )
        
        # Step 4: Recreate AES key using cloud metadata
        metadata = f"{workload_package['cloud_region']}:{workload_package['workload_type']}".encode('utf-8')
        aes_key = self._derive_cloud_specific_key(shared_secret, metadata)
        
        # Step 5: Decrypt workload data
        decrypted_data = self.aes_manager.decrypt_data(
            workload_package["encrypted_data"], 
            aes_key
        )
        
        decryption_time = time.time() - start_time
        
        return {
            "data": decrypted_data,
            "metadata": {
                "cloud_region": workload_package["cloud_region"],
                "workload_type": workload_package["workload_type"],
                "original_timestamp": workload_package["timestamp"],
                "decryption_time": decryption_time
            }
        }
    
    def _derive_cloud_specific_key(self, shared_secret, metadata):
        """
        NOVELTY: Cloud-specific key derivation.
        Combines shared secret with cloud metadata for enhanced security.
        """
        from cryptography.hazmat.primitives.kdf.hkdf import HKDF
        from cryptography.hazmat.primitives import hashes
        
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,  # 256-bit AES key
            salt=metadata,  # Use cloud metadata as salt
            info=b'hybrid-ecc-aes-cloud-workload'
        ).derive(shared_secret)
        
        return derived_key
    
    def encrypt_large_workload(self, file_path, cloud_region="us-east-1", workload_type="batch"):
        """
        NOVELTY: Optimized encryption for large cloud workloads (files).
        Uses streaming encryption for memory efficiency.
        """
        import os
        
        start_time = time.time()
        file_size = os.path.getsize(file_path)
        
        # Generate keys
        client_private_key, client_public_key = self.ecc_manager.generate_key_pair()
        shared_secret = self.ecc_manager.derive_shared_key(client_private_key, self.server_public_key)
        
        metadata = f"{cloud_region}:{workload_type}".encode('utf-8')
        aes_key = self._derive_cloud_specific_key(shared_secret, metadata)
        
        # Encrypt file
        encrypted_file_path = self.aes_manager.encrypt_file(file_path, aes_key)
        
        encryption_time = time.time() - start_time
        
        # Create metadata package
        metadata_package = {
            "client_public_key": self.ecc_manager.serialize_public_key(client_public_key).decode('utf-8'),
            "cloud_region": cloud_region,
            "workload_type": workload_type,
            "original_file_size": file_size,
            "encrypted_file_path": encrypted_file_path,
            "encryption_time": encryption_time,
            "timestamp": time.time()
        }
        
        return metadata_package, encrypted_file_path
