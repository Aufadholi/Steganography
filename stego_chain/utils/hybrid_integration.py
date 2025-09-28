"""
Hybrid Steganography-Blockchain Integration Module
Menghubungkan LSB Steganography dengan Blockchain untuk dual-channel security
"""

import os
import json
from datetime import datetime
from typing import Dict, Optional
from .lsb_steganography import LSBSteganography
from ..core.blockchain import send_transaction, get_transaction_data, check_connection

class HybridSteganographyBlockchain:
    """Hybrid system yang menggabungkan LSB steganography dengan blockchain verification"""
    
    def __init__(self):
        self.lsb = LSBSteganography()
        self.reports_dir = "reports"
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Buat direktori yang diperlukan"""
        directories = [self.reports_dir, "output", "temp"]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def send_secure_message(self, cover_image_path: str, secret_message: str, 
                          recipient_address: str, password: str = None) -> Dict:
        """
        Complete hybrid steganography-blockchain workflow untuk mengirim pesan
        
        Args:
            cover_image_path: Path gambar cover
            secret_message: Pesan rahasia  
            recipient_address: Alamat blockchain penerima
            password: Password enkripsi (optional)
            
        Returns:
            Dict hasil proses lengkap
        """
        try:
            print("🚀 === HYBRID STEGANOGRAPHY-BLOCKCHAIN SYSTEM ===")
            print("📤 Memulai pengiriman pesan aman...")
            
            # Step 1: LSB Steganography
            stego_image_path = f"output/stego_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            print("\n🔒 STEP 1: LSB STEGANOGRAPHY")
            embed_result = self.lsb.embed_message(
                cover_image_path, secret_message, stego_image_path, password
            )
            
            if not embed_result['success']:
                return {'success': False, 'error': f"LSB embedding failed: {embed_result['error']}"}
            
            # Step 2: Blockchain Hash Storage
            print("\n🔗 STEP 2: BLOCKCHAIN VERIFICATION")
            
            if not check_connection():
                return {'success': False, 'error': "Blockchain connection failed"}
            
            file_hash = embed_result['file_hash']
            print(f"📋 Sending image hash to blockchain: {file_hash[:16]}...")
            
            try:
                tx_hash = send_transaction(recipient_address, file_hash)
                print(f"✅ Blockchain transaction successful!")
                print(f"🔗 Transaction hash: {tx_hash}")
                print(f"🌐 Explorer: https://sepolia.etherscan.io/tx/{tx_hash}")
            except Exception as e:
                return {'success': False, 'error': f"Blockchain transaction failed: {str(e)}"}
            
            # Step 3: Generate Transfer Instructions
            print("\n📧 STEP 3: TRANSFER INSTRUCTIONS")
            transfer_data = self._generate_transfer_instructions(
                stego_image_path, tx_hash, embed_result, recipient_address
            )
            
            # Step 4: Generate Report
            report_path = self._generate_report({
                'cover_image': cover_image_path,
                'stego_image': stego_image_path,
                'message_length': len(secret_message),
                'embed_result': embed_result,
                'tx_hash': tx_hash,
                'recipient': recipient_address,
                'transfer_data': transfer_data
            })
            
            print(f"\n📊 Process completed successfully!")
            print(f"📄 Report saved: {report_path}")
            print(f"📁 Stego image: {stego_image_path}")
            print(f"📋 Transfer instructions: {transfer_data['instructions_file']}")
            
            return {
                'success': True,
                'stego_image_path': stego_image_path,
                'blockchain_tx_hash': tx_hash,
                'file_hash': file_hash,
                'transfer_instructions': transfer_data,
                'embed_metrics': embed_result['metrics'],
                'report_path': report_path
            }
            
        except Exception as e:
            print(f"❌ Hybrid system error: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def receive_secure_message(self, stego_image_path: str, blockchain_tx_hash: str, 
                             password: str = None) -> Dict:
        """
        Complete hybrid workflow untuk menerima dan memverifikasi pesan
        
        Args:
            stego_image_path: Path gambar stego yang diterima
            blockchain_tx_hash: Hash transaksi blockchain
            password: Password dekripsi (optional)
            
        Returns:
            Dict hasil ekstraksi dan verifikasi
        """
        try:
            print("🚀 === MESSAGE EXTRACTION & VERIFICATION ===")
            print("📥 Memulai ekstraksi dan verifikasi pesan...")
            
            # Step 1: LSB Message Extraction
            print("\n🔍 STEP 1: LSB MESSAGE EXTRACTION")
            extract_result = self.lsb.extract_message(stego_image_path, password)
            
            if not extract_result['success']:
                return {'success': False, 'error': f"Message extraction failed: {extract_result['error']}"}
            
            # Step 2: Blockchain Integrity Verification
            print("\n🔗 STEP 2: BLOCKCHAIN INTEGRITY VERIFICATION")
            
            if not check_connection():
                print("⚠️ Warning: Blockchain connection failed - cannot verify integrity")
                integrity_verified = False
                blockchain_hash = None
            else:
                try:
                    blockchain_data = get_transaction_data(blockchain_tx_hash)
                    blockchain_hash = blockchain_data if blockchain_data else None
                    
                    if blockchain_hash:
                        # Remove '0x' prefix if present
                        if blockchain_hash.startswith('0x'):
                            blockchain_hash = blockchain_hash[2:]
                        
                        current_hash = extract_result['file_hash']
                        integrity_verified = (blockchain_hash.lower() == current_hash.lower())
                        
                        print(f"📋 Blockchain hash: {blockchain_hash[:16]}...")
                        print(f"📋 Current hash:   {current_hash[:16]}...")
                        
                        if integrity_verified:
                            print("✅ INTEGRITY VERIFIED - Image is authentic!")
                        else:
                            print("❌ INTEGRITY COMPROMISED - Image may be tampered!")
                    else:
                        print("⚠️ Could not retrieve hash from blockchain")
                        integrity_verified = False
                        
                except Exception as e:
                    print(f"⚠️ Blockchain verification error: {str(e)}")
                    integrity_verified = False
                    blockchain_hash = None
            
            # Step 3: Generate Verification Report
            verification_report = self._generate_verification_report({
                'stego_image': stego_image_path,
                'extracted_message': extract_result['message'],
                'blockchain_tx_hash': blockchain_tx_hash,
                'blockchain_hash': blockchain_hash,
                'current_hash': extract_result['file_hash'],
                'integrity_verified': integrity_verified,
                'extract_result': extract_result
            })
            
            print(f"\n📊 Extraction completed!")
            print(f"📝 Message: '{extract_result['message']}'")
            print(f"🔒 Security status: {'VERIFIED' if integrity_verified else 'UNVERIFIED'}")
            print(f"📄 Verification report: {verification_report}")
            
            return {
                'success': True,
                'message': extract_result['message'],
                'integrity_verified': integrity_verified,
                'blockchain_tx_hash': blockchain_tx_hash,
                'blockchain_hash': blockchain_hash,
                'current_file_hash': extract_result['file_hash'],
                'verification_report': verification_report,
                'message_length': extract_result['message_length']
            }
            
        except Exception as e:
            print(f"❌ Message reception error: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _generate_transfer_instructions(self, stego_image_path: str, tx_hash: str, 
                                      embed_result: Dict, recipient: str) -> Dict:
        """Generate instruksi transfer untuk penerima"""
        instructions = {
            'sender_info': {
                'stego_image_file': os.path.basename(stego_image_path),
                'blockchain_tx_hash': tx_hash,
                'image_hash': embed_result['file_hash'],
                'timestamp': datetime.now().isoformat()
            },
            'recipient_instructions': [
                "1. Save gambar stego yang diterima",
                "2. Copy transaction hash dari MetaMask atau instruksi ini",  
                "3. Jalankan aplikasi ekstraksi",
                "4. Input path gambar dan transaction hash",
                "5. Verifikasi integritas melalui blockchain"
            ],
            'security_info': {
                'pixels_modified': embed_result['pixels_modified'],
                'modification_rate': f"{embed_result['modification_rate']:.3f}%",
                'psnr': f"{embed_result['metrics']['psnr']:.2f} dB",
                'encrypted': embed_result['encrypted']
            }
        }
        
        # Save instructions to file
        instructions_file = f"output/transfer_instructions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(instructions_file, 'w') as f:
            json.dump(instructions, f, indent=2)
        
        # Create simple text instructions
        text_instructions = f"""
=== HYBRID STEGANOGRAPHY TRANSFER INSTRUCTIONS ===

UNTUK PENERIMA ({recipient}):

1. 📁 TERIMA FILE:
   - Stego Image: {os.path.basename(stego_image_path)}
   - Ukuran: {os.path.getsize(stego_image_path)} bytes
   
2. 🔗 BLOCKCHAIN INFO:
   - Transaction Hash: {tx_hash}
   - Image Hash: {embed_result['file_hash'][:16]}...
   - Explorer: https://sepolia.etherscan.io/tx/{tx_hash}
   
3. 📱 METMASK CHECK:
   - Buka MetaMask penerima  
   - Cek Activity → ada transaksi masuk
   - Copy transaction hash jika diperlukan
   
4. 🔓 EKSTRAKSI:
   - Jalankan aplikasi steganografi
   - Input stego image path
   - Input transaction hash: {tx_hash}
   - Dapatkan pesan tersembunyi!
   
5. ✅ VERIFIKASI:
   - System akan auto-verify integrity via blockchain
   - Status VERIFIED = image authentic
   - Status UNVERIFIED = possible tampering

=== SECURITY METRICS ===
- PSNR: {embed_result['metrics']['psnr']:.2f} dB (Excellent)
- Pixels Modified: {embed_result['pixels_modified']:,} ({embed_result['modification_rate']:.3f}%)
- Encryption: {"Yes" if embed_result['encrypted'] else "No"}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        text_file = f"output/instructions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(text_instructions)
        
        return {
            'instructions_file': instructions_file,
            'text_file': text_file,
            'data': instructions
        }
    
    def _generate_report(self, data: Dict) -> str:
        """Generate comprehensive report untuk dokumentasi"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'process_type': 'HYBRID_STEGANOGRAPHY_SEND',
            'input': {
                'cover_image': data['cover_image'],
                'message_length': data['message_length'],
                'recipient': data['recipient']
            },
            'output': {
                'stego_image': data['stego_image'],
                'blockchain_tx_hash': data['tx_hash'],
                'file_hash': data['embed_result']['file_hash']
            },
            'steganography_metrics': data['embed_result']['metrics'],
            'blockchain_info': {
                'transaction_hash': data['tx_hash'],
                'explorer_url': f"https://sepolia.etherscan.io/tx/{data['tx_hash']}",
                'recipient_address': data['recipient']
            },
            'security_analysis': {
                'pixels_modified': data['embed_result']['pixels_modified'],
                'modification_rate': data['embed_result']['modification_rate'],
                'detectability': 'Very Low' if data['embed_result']['metrics']['psnr'] > 40 else 'Low',
                'integrity_protection': 'Blockchain-verified'
            }
        }
        
        report_file = f"{self.reports_dir}/send_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report_file
    
    def _generate_verification_report(self, data: Dict) -> str:
        """Generate verification report untuk dokumentasi"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'process_type': 'HYBRID_STEGANOGRAPHY_RECEIVE',
            'input': {
                'stego_image': data['stego_image'],
                'blockchain_tx_hash': data['blockchain_tx_hash']
            },
            'extraction_result': {
                'message_extracted': data['extracted_message'],
                'message_length': len(data['extracted_message']),
                'extraction_successful': True
            },
            'integrity_verification': {
                'blockchain_hash': data['blockchain_hash'],
                'current_file_hash': data['current_hash'],
                'integrity_verified': data['integrity_verified'],
                'verification_method': 'SHA256_BLOCKCHAIN_COMPARISON'
            },
            'security_status': {
                'overall_status': 'SECURE' if data['integrity_verified'] else 'COMPROMISED',
                'tampering_detected': not data['integrity_verified'],
                'blockchain_verified': data['integrity_verified']
            }
        }
        
        report_file = f"{self.reports_dir}/verification_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report_file


# =============================================
# STANDALONE FUNCTIONS FOR GUI COMPATIBILITY
# =============================================

# Global instance for standalone functions
_hybrid_system = None

def _get_hybrid_system():
    """Get or create hybrid system instance"""
    global _hybrid_system
    if _hybrid_system is None:
        _hybrid_system = HybridSteganographyBlockchain()
    return _hybrid_system

def send_secure_message(cover_image_path: str, secret_message: str, 
                       recipient_address: str, output_path: str = None, 
                       password: str = None) -> Dict:
    """
    Standalone function untuk GUI compatibility
    Send secure message using hybrid steganography-blockchain system
    
    Args:
        cover_image_path: Path to cover image
        secret_message: Secret message to embed
        recipient_address: Blockchain recipient address
        output_path: Custom output path (optional)
        password: Encryption password (optional)
        
    Returns:
        Dict with success status, paths, metrics, etc.
    """
    try:
        hybrid = _get_hybrid_system()
        result = hybrid.send_secure_message(
            cover_image_path=cover_image_path,
            secret_message=secret_message,
            recipient_address=recipient_address,
            password=password
        )
        
        # If custom output path specified, copy the stego image
        if output_path and result.get('success') and result.get('stego_image_path'):
            import shutil
            try:
                shutil.copy2(result['stego_image_path'], output_path)
                result['stego_path'] = output_path
            except Exception as e:
                print(f"⚠️ Warning: Could not copy to custom path: {e}")
                result['stego_path'] = result['stego_image_path']
        else:
            result['stego_path'] = result.get('stego_image_path')
            
        # Add GUI-friendly keys
        if result.get('success'):
            result['tx_hash'] = result.get('blockchain_tx_hash')
            result['metrics'] = result.get('embed_metrics', {})
            
        return result
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def receive_secure_message(stego_image_path: str, tx_hash: str = None, 
                          password: str = None) -> Dict:
    """
    Standalone function untuk GUI compatibility  
    Receive and verify secure message from stego image
    
    Args:
        stego_image_path: Path to stego image
        tx_hash: Blockchain transaction hash for verification (optional)
        password: Decryption password (optional)
        
    Returns:
        Dict with extracted message, verification status, etc.
    """
    try:
        hybrid = _get_hybrid_system()
        
        if tx_hash:
            result = hybrid.receive_secure_message(
                stego_image_path=stego_image_path,
                blockchain_tx_hash=tx_hash,
                password=password
            )
        else:
            # Extract without blockchain verification
            result = hybrid.lsb.extract_message(stego_image_path, password)
            if result.get('success'):
                result['verified'] = False
                result['message'] = result.get('extracted_message', '')
            
        return result
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }