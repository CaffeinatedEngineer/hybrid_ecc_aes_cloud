from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
import hashlib

class AESManager:
    def __init__(self, key_size=256):
        """Initialize AES manager."""
        self.key_size = key_size // 8  # Convert bits to bytes
        self.block_size = AES.block_size
    
    def generate_aes_key(self):
        """Generate random AES key."""
        return get_random_bytes(self.key_size)
    
    def encrypt_data(self, data, key):
        """Encrypt data using AES-CBC."""
        # Convert string to bytes if necessary
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        # Generate random IV
        iv = get_random_bytes(self.block_size)
        
        # Create cipher and encrypt
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_data = pad(data, self.block_size)
        encrypted_data = cipher.encrypt(padded_data)
        
        # Combine IV and encrypted data
        result = iv + encrypted_data
        return base64.b64encode(result).decode('utf-8')
    
    def decrypt_data(self, encrypted_data, key):
        """Decrypt AES-encrypted data."""
        # Decode base64
        encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
        
        # Extract IV and encrypted data
        iv = encrypted_bytes[:self.block_size]
        encrypted_content = encrypted_bytes[self.block_size:]
        
        # Decrypt
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_padded = cipher.decrypt(encrypted_content)
        decrypted_data = unpad(decrypted_padded, self.block_size)
        
        return decrypted_data.decode('utf-8')
    
    def encrypt_file(self, file_path, key, output_path=None):
        """Encrypt a file using AES."""
        if output_path is None:
            output_path = file_path + '.encrypted'
        
        iv = get_random_bytes(self.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        with open(file_path, 'rb') as infile, open(output_path, 'wb') as outfile:
            outfile.write(iv)  # Write IV first
            
            while True:
                chunk = infile.read(8192)  # 8KB chunks
                if len(chunk) == 0:
                    break
                elif len(chunk) % self.block_size != 0:
                    chunk = pad(chunk, self.block_size)
                
                encrypted_chunk = cipher.encrypt(chunk)
                outfile.write(encrypted_chunk)
        
        return output_path
