"""
LSB (Least Significant Bit) Steganography Module
Untuk menyembunyikan dan mengekstrak pesan dalam gambar
Part of: Hybrid LSB Steganography-Blockchain System
"""

from PIL import Image
import numpy as np
import hashlib
import os
from typing import Tuple, Optional

class LSBSteganography:
    """Class untuk melakukan LSB steganography pada gambar"""
    
    def __init__(self):
        self.delimiter = "###END_OF_MESSAGE###"
        self.supported_formats = ['.png', '.bmp', '.tiff']
    
    def text_to_binary(self, text: str) -> str:
        """Konversi text ke binary string"""
        binary = ''.join(format(ord(char), '08b') for char in text)
        return binary
    
    def binary_to_text(self, binary: str) -> str:
        """Konversi binary string ke text"""
        text = ''
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) == 8:
                try:
                    char = chr(int(byte, 2))
                    text += char
                except ValueError:
                    break
        return text
    
    def embed_message(self, cover_image_path: str, secret_message: str, 
                     stego_image_path: str, password: str = None) -> dict:
        """
        Menyembunyikan pesan dalam gambar menggunakan LSB
        
        Args:
            cover_image_path: Path gambar cover
            secret_message: Pesan yang akan disembunyikan
            stego_image_path: Path output gambar stego
            password: Password untuk enkripsi (optional)
            
        Returns:
            dict: Hasil proses embedding dengan metrics
        """
        try:
            print("🔒 Memulai LSB Embedding...")
            
            # Validasi file
            if not os.path.exists(cover_image_path):
                raise FileNotFoundError(f"Cover image tidak ditemukan: {cover_image_path}")
            
            # Load dan validasi gambar
            image = Image.open(cover_image_path).convert('RGB')
            print(f"📁 Gambar loaded: {image.size[0]}x{image.size[1]} pixels")
            
            # Enkripsi pesan jika ada password
            if password:
                secret_message = self._encrypt_message(secret_message, password)
                print(f"🔐 Pesan dienkripsi dengan password")
            
            # Tambahkan delimiter
            message_with_delimiter = secret_message + self.delimiter
            
            # Konversi ke binary
            binary_message = self.text_to_binary(message_with_delimiter)
            print(f"📝 Pesan length: {len(secret_message)} chars → {len(binary_message)} bits")
            
            # Cek kapasitas
            pixels = np.array(image)
            total_pixels = pixels.shape[0] * pixels.shape[1] * 3  # RGB channels
            
            if len(binary_message) > total_pixels:
                raise ValueError(f"Pesan terlalu panjang! Butuh {len(binary_message)} bits, tersedia {total_pixels}")
            
            # LSB embedding
            modified_pixels = self._embed_lsb(pixels.copy(), binary_message)
            pixels_changed = int(np.sum(pixels != modified_pixels))
            
            # Save stego image
            stego_image = Image.fromarray(modified_pixels.astype('uint8'))
            stego_image.save(stego_image_path)
            
            # Calculate metrics
            metrics = self._calculate_metrics(pixels, modified_pixels)
            
            # Calculate file hash
            file_hash = self._calculate_file_hash(stego_image_path)
            
            print(f"✅ LSB embedding berhasil!")
            print(f"💾 Stego image saved: {stego_image_path}")
            print(f"📊 Pixels modified: {pixels_changed:,} ({pixels_changed/total_pixels*100:.3f}%)")
            print(f"📈 PSNR: {metrics['psnr']:.2f} dB")
            print(f"📉 MSE: {metrics['mse']:.2f}")
            print(f"🔑 File hash: {file_hash[:16]}...")
            
            return {
                'success': True,
                'stego_image_path': stego_image_path,
                'file_hash': file_hash,
                'message_length': len(secret_message),
                'pixels_modified': pixels_changed,
                'modification_rate': float(pixels_changed/total_pixels*100),
                'metrics': metrics,
                'encrypted': password is not None
            }
            
        except Exception as e:
            print(f"❌ Error dalam LSB embedding: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def extract_message(self, stego_image_path: str, password: str = None) -> dict:
        """
        Mengekstrak pesan tersembunyi dari gambar stego
        
        Args:
            stego_image_path: Path gambar stego
            password: Password untuk dekripsi (optional)
            
        Returns:
            dict: Hasil ekstraksi pesan
        """
        try:
            print("🔍 Memulai LSB Extraction...")
            
            # Validasi file
            if not os.path.exists(stego_image_path):
                raise FileNotFoundError(f"Stego image tidak ditemukan: {stego_image_path}")
            
            # Load gambar
            image = Image.open(stego_image_path).convert('RGB')
            pixels = np.array(image)
            print(f"📁 Stego image loaded: {image.size[0]}x{image.size[1]} pixels")
            
            # Extract binary data dari LSB
            binary_message = self._extract_lsb(pixels)
            
            # Konversi ke text
            extracted_text = self.binary_to_text(binary_message)
            
            # Cari delimiter
            if self.delimiter in extracted_text:
                secret_message = extracted_text.split(self.delimiter)[0]
                
                # Dekripsi jika ada password
                if password:
                    secret_message = self._decrypt_message(secret_message, password)
                    print(f"🔓 Pesan didekripsi")
                
                # Calculate file hash untuk verifikasi
                file_hash = self._calculate_file_hash(stego_image_path)
                
                print(f"✅ Pesan berhasil diekstrak!")
                print(f"📝 Message length: {len(secret_message)} characters")
                print(f"🔑 File hash: {file_hash[:16]}...")
                
                return {
                    'success': True,
                    'message': secret_message,
                    'file_hash': file_hash,
                    'message_length': len(secret_message),
                    'decrypted': password is not None
                }
            else:
                raise ValueError("Delimiter tidak ditemukan - mungkin bukan stego image atau password salah")
                
        except Exception as e:
            print(f"❌ Error dalam LSB extraction: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _embed_lsb(self, pixels: np.ndarray, binary_message: str) -> np.ndarray:
        """Embed binary message ke LSB pixels"""
        flat_pixels = pixels.flatten()
        
        for i, bit in enumerate(binary_message):
            if i < len(flat_pixels):
                # Modify LSB
                flat_pixels[i] = (flat_pixels[i] & 0xFE) | int(bit)
        
        return flat_pixels.reshape(pixels.shape)
    
    def _extract_lsb(self, pixels: np.ndarray) -> str:
        """Extract binary message dari LSB pixels"""
        flat_pixels = pixels.flatten()
        binary_message = ""
        
        for pixel in flat_pixels:
            binary_message += str(pixel & 1)
            
            # Check untuk delimiter setiap 8 bits
            if len(binary_message) % 8 == 0:
                current_text = self.binary_to_text(binary_message)
                if self.delimiter in current_text:
                    break
        
        return binary_message
    
    def _calculate_metrics(self, original: np.ndarray, modified: np.ndarray) -> dict:
        """Calculate PSNR, MSE, dan SSIM"""
        # MSE (Mean Square Error)
        mse = float(np.mean((original.astype(float) - modified.astype(float)) ** 2))
        
        # PSNR (Peak Signal-to-Noise Ratio)  
        if mse == 0:
            psnr = float('inf')
        else:
            psnr = float(20 * np.log10(255.0 / np.sqrt(mse)))
        
        # SSIM estimation (simplified)
        ssim = float(1 - (mse / (255.0 ** 2)))
        
        return {
            'mse': mse,
            'psnr': psnr,
            'ssim': max(0.0, min(1.0, ssim))
        }
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA256 hash dari file"""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    
    def _encrypt_message(self, message: str, password: str) -> str:
        """Simple XOR encryption"""
        key = hashlib.sha256(password.encode()).digest()
        encrypted = ""
        for i, char in enumerate(message):
            encrypted += chr(ord(char) ^ key[i % len(key)])
        return encrypted
    
    def _decrypt_message(self, encrypted_message: str, password: str) -> str:
        """Simple XOR decryption"""
        return self._encrypt_message(encrypted_message, password)  # XOR is symmetric

# Utility functions
def validate_image_format(image_path: str) -> bool:
    """Validasi format gambar yang didukung"""
    supported = ['.png', '.bmp', '.tiff']
    return any(image_path.lower().endswith(ext) for ext in supported)

def get_image_info(image_path: str) -> dict:
    """Get informasi dasar gambar"""
    try:
        with Image.open(image_path) as img:
            return {
                'size': img.size,
                'mode': img.mode,
                'format': img.format,
                'file_size': os.path.getsize(image_path)
            }
    except Exception as e:
        return {'error': str(e)}