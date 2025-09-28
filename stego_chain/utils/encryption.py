from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import hashlib

def encrypt(data, key):
    """Encrypt data menggunakan AES-256-CBC"""
    print(f"-> (Encrypting with key: {key})")
    
    # Buat key 256-bit dari string key
    key_hash = hashlib.sha256(key.encode()).digest()
    
    # Generate IV random
    iv = get_random_bytes(16)
    
    # Encrypt dengan AES
    cipher = AES.new(key_hash, AES.MODE_CBC, iv)
    padded_data = pad(data, AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    
    # Return IV + encrypted data
    return iv + encrypted_data

def decrypt(data, key):
    """Decrypt data menggunakan AES-256-CBC"""
    print(f"-> (Decrypting with key: {key})")
    
    try:
        # Validasi ukuran data minimum
        if len(data) < 32:  # IV (16) + minimal encrypted block (16)
            raise ValueError(f"Data terlalu pendek: {len(data)} bytes, minimal 32 bytes")
        
        # Buat key 256-bit dari string key
        key_hash = hashlib.sha256(key.encode()).digest()
        
        # Extract IV dan encrypted data
        iv = data[:16]
        encrypted_data = data[16:]
        
        # Validasi ukuran encrypted data harus kelipatan 16
        if len(encrypted_data) % 16 != 0:
            raise ValueError(f"Encrypted data tidak valid: {len(encrypted_data)} bytes (harus kelipatan 16)")
        
        print(f"🔐 IV: {iv.hex()[:16]}...")
        print(f"📦 Encrypted: {len(encrypted_data)} bytes")
        
        # Decrypt dengan AES
        cipher = AES.new(key_hash, AES.MODE_CBC, iv)
        decrypted_padded = cipher.decrypt(encrypted_data)
        decrypted_data = unpad(decrypted_padded, AES.block_size)
        
        print(f"✅ Berhasil dekripsi: {len(decrypted_data)} bytes")
        return decrypted_data
        
    except ValueError as e:
        print(f"❌ Padding Error: {str(e)}")
        print(f"💡 Kemungkinan kunci salah atau data corrupted")
        raise e
    except Exception as e:
        print(f"❌ Dekripsi Error: {str(e)}")
        print(f"💡 Pastikan menggunakan kunci yang sama saat enkripsi")
        raise e