#!/usr/bin/env python3
"""
Real Email Integration for Steganography System
Kirim file stego via SMTP dengan attachment real
Support Gmail, Outlook, Yahoo dengan App Password
"""

import smtplib
import ssl
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import json
import re
from typing import Dict, Optional

class RealEmailSender:
    """Real email sender menggunakan SMTP dengan multiple provider support"""
    
    def __init__(self):
        self.email_providers = {
            'gmail': {
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587,
                'requires_app_password': True
            },
            'outlook': {
                'smtp_server': 'smtp-mail.outlook.com', 
                'smtp_port': 587,
                'requires_app_password': False
            },
            'yahoo': {
                'smtp_server': 'smtp.mail.yahoo.com',
                'smtp_port': 587,
                'requires_app_password': True
            }
        }
        self._ensure_directories()
        
    def _ensure_directories(self):
        """Buat direktori yang diperlukan"""
        directories = ["logs", "email_templates"]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def detect_email_provider(self, email: str) -> str:
        """Auto-detect email provider dari email address"""
        domain = email.lower().split('@')[1]
        
        if 'gmail.com' in domain:
            return 'gmail'
        elif 'outlook.com' in domain or 'hotmail.com' in domain or 'live.com' in domain:
            return 'outlook'
        elif 'yahoo.com' in domain:
            return 'yahoo'
        else:
            return 'gmail'  # Default fallback
    
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def send_stego_email(self, sender_email: str, sender_password: str, 
                        recipient_email: str, stego_image_path: str, 
                        tx_hash: str, secret_message_preview: str = "", 
                        subject: str = None) -> Dict:
        """
        Kirim email real dengan attachment stego image
        
        Args:
            sender_email: Email pengirim
            sender_password: Password/App Password  
            recipient_email: Email tujuan
            stego_image_path: Path file stego image
            tx_hash: Blockchain transaction hash
            secret_message_preview: Preview pesan untuk logging
            subject: Custom subject (optional)
            
        Returns:
            Dict hasil pengiriman
        """
        try:
            print(f"📧 Starting real email transmission...")
            print(f"   From: {sender_email}")
            print(f"   To: {recipient_email}")
            
            # Validasi inputs
            if not self.validate_email(sender_email):
                return {'success': False, 'error': 'Invalid sender email format'}
            
            if not self.validate_email(recipient_email):
                return {'success': False, 'error': 'Invalid recipient email format'}
                
            if not os.path.exists(stego_image_path):
                return {'success': False, 'error': 'Stego image file not found'}
            
            # Detect email provider
            provider = self.detect_email_provider(sender_email)
            smtp_config = self.email_providers[provider]
            
            print(f"   Provider: {provider.upper()}")
            print(f"   SMTP: {smtp_config['smtp_server']}:{smtp_config['smtp_port']}")
            
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject or "🔐 Secure Document - Steganography Transfer"
            
            # Create professional email body
            body = self._create_professional_email_body(
                tx_hash, stego_image_path, sender_email, secret_message_preview
            )
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach stego image
            attachment_result = self._attach_stego_image(msg, stego_image_path)
            if not attachment_result['success']:
                return attachment_result
            
            print(f"   📎 Attachment: {os.path.basename(stego_image_path)} ({attachment_result['file_size']} bytes)")
            
            # Send email via SMTP
            context = ssl.create_default_context()
            
            with smtplib.SMTP(smtp_config['smtp_server'], smtp_config['smtp_port']) as server:
                server.starttls(context=context)
                server.login(sender_email, sender_password)
                
                text = msg.as_string()
                server.sendmail(sender_email, recipient_email, text)
            
            # Log successful send
            log_data = self._log_email_transmission(
                sender_email, recipient_email, tx_hash, 
                stego_image_path, secret_message_preview
            )
            
            print(f"✅ Real email sent successfully!")
            print(f"   📧 Email delivered to: {recipient_email}")
            print(f"   🔗 Blockchain TX: {tx_hash[:16]}...")
            print(f"   📄 Log saved: {log_data['log_file']}")
            
            return {
                'success': True,
                'sender': sender_email,
                'recipient': recipient_email,
                'tx_hash': tx_hash,
                'attachment': os.path.basename(stego_image_path),
                'file_size': attachment_result['file_size'],
                'provider': provider,
                'timestamp': datetime.now().isoformat(),
                'log_file': log_data['log_file']
            }
            
        except smtplib.SMTPAuthenticationError as e:
            error_msg = f"Email authentication failed: {str(e)}\n\n"
            if 'gmail' in sender_email.lower():
                error_msg += "📧 Gmail Users:\n• Use App Password (not regular password)\n• Enable 2-Step Verification\n• Generate App Password in Google Account settings"
            elif 'outlook' in sender_email.lower():
                error_msg += "📧 Outlook Users:\n• Use regular password (App Password not required)\n• Enable 'Less secure app access' if needed"
            else:
                error_msg += "📧 Please check:\n• Email and password are correct\n• 2FA and App Passwords if required\n• SMTP settings for your provider"
                
            return {'success': False, 'error': error_msg}
            
        except smtplib.SMTPRecipientsRefused as e:
            return {'success': False, 'error': f"Recipient email rejected: {str(e)}"}
            
        except smtplib.SMTPServerDisconnected as e:
            return {'success': False, 'error': f"SMTP server disconnected: {str(e)}"}
            
        except Exception as e:
            return {'success': False, 'error': f"Email sending failed: {str(e)}"}
    
    def _create_professional_email_body(self, tx_hash: str, stego_image_path: str, 
                                       sender_email: str, message_preview: str = "") -> str:
        """Create professional email body dengan instructions"""
        filename = os.path.basename(stego_image_path)
        file_size = os.path.getsize(stego_image_path)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Preview message untuk context (tanpa reveal full message)
        preview_text = ""
        if message_preview and len(message_preview) > 0:
            preview_length = min(20, len(message_preview))
            preview_text = f"\n• Message Preview: \"{message_preview[:preview_length]}{'...' if len(message_preview) > preview_length else '\"'}"
        
        body = f"""🔐 HYBRID STEGANOGRAPHY SECURE TRANSMISSION

Dear Recipient,

You have received a secure document using our Hybrid LSB Steganography-Blockchain system.

📄 DOCUMENT INFORMATION:
• Filename: {filename}
• File Size: {file_size:,} bytes
• Transmission Time: {timestamp}
• Type: Steganographic image with hidden message{preview_text}

🔗 BLOCKCHAIN VERIFICATION:
• Transaction Hash: {tx_hash}
• Blockchain Network: Ethereum Sepolia Testnet  
• Explorer Link: https://sepolia.etherscan.io/tx/{tx_hash}
• Sender Address: 0x03C779967c8581e092570e5d77832dFF7cF9ae27
• Receiver Address: 0x50E57867322143f349d55197388Db32d1b7DB8e5

📋 MESSAGE EXTRACTION INSTRUCTIONS:
1. Download the attached image file to your computer
2. Use the Steganography Extraction Tool or GUI
3. Load the downloaded image in the extraction interface
4. Input the blockchain transaction hash above for verification
5. Click "Extract & Verify Message" to reveal the hidden content

⚠️ SECURITY INFORMATION:
• The attached image appears completely normal to the human eye
• It contains a secret message embedded using LSB (Least Significant Bit) technique
• The blockchain transaction hash ensures message integrity verification
• This dual-channel approach provides enhanced security for sensitive communications

🔧 TECHNICAL SPECIFICATIONS:
• Steganography Method: LSB (Least Significant Bit)
• Image Format: PNG (lossless compression for data preservation)
• Blockchain: Ethereum Sepolia Testnet for integrity verification
• Security Level: Dual-channel (Visual + Blockchain) verification

📞 SUPPORT:
If you need assistance with message extraction or have questions about this secure transfer system, please reply to this email or contact: {sender_email}

---
🔬 Research Note: This system is part of academic research on "Hybrid LSB Steganography-Blockchain System for Secure Digital Communication with Integrity Verification" - a novel approach combining visual steganography with blockchain technology for enhanced security.

Sent via Hybrid LSB Steganography-Blockchain System
Developed for Advanced Digital Security Research
        """.strip()
        
        return body
    
    def _attach_stego_image(self, msg: MIMEMultipart, file_path: str) -> Dict:
        """Attach stego image file to email message"""
        try:
            with open(file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {filename}'
            )
            
            msg.attach(part)
            
            return {
                'success': True,
                'filename': filename,
                'file_size': file_size
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to attach file: {str(e)}"
            }
    
    def _log_email_transmission(self, sender: str, recipient: str, tx_hash: str, 
                               file_path: str, message_preview: str = "") -> Dict:
        """Log email transmission untuk tracking dan research"""
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'sender_email': sender,
                'recipient_email': recipient,
                'tx_hash': tx_hash,
                'stego_filename': os.path.basename(file_path),
                'file_size': os.path.getsize(file_path),
                'message_preview': message_preview[:50] + "..." if len(message_preview) > 50 else message_preview,
                'provider': self.detect_email_provider(sender),
                'blockchain_network': 'Ethereum Sepolia',
                'system_version': 'Hybrid LSB Steganography-Blockchain v1.0'
            }
            
            # Save to main log file
            log_file = "logs/email_transmissions.json"
            
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            else:
                logs = []
            
            logs.append(log_entry)
            
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)
            
            # Save individual transmission report
            report_file = f"logs/transmission_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_file, 'w') as f:
                json.dump(log_entry, f, indent=2)
                
            return {
                'success': True,
                'log_file': log_file,
                'report_file': report_file
            }
            
        except Exception as e:
            print(f"Warning: Failed to log email transmission: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_gmail_app_password_guide(self) -> str:
        """Return detailed guide untuk setup Gmail App Password"""
        return """
🔧 GMAIL APP PASSWORD SETUP GUIDE:

📋 Step-by-Step Instructions:
1. Go to Google Account: https://myaccount.google.com/
2. Click "Security" in left sidebar
3. Under "Signing in to Google" → click "2-Step Verification"
4. Enable 2-Step Verification if not already enabled
5. Go back to Security → click "App passwords"
6. Select app: "Mail" 
7. Select device: "Windows Computer"
8. Click "Generate"
9. Copy the generated 16-character password (format: abcd efgh ijkl mnop)
10. Use this App Password in the application (NOT your regular Gmail password)

⚠️ IMPORTANT NOTES:
• MUST use App Password, not regular Gmail password
• 2-Step Verification must be enabled first  
• Regular Gmail password will NOT work for SMTP
• Keep App Password secure and don't share it

🔍 Troubleshooting:
• If "App passwords" option is not visible, ensure 2-Step Verification is fully enabled
• If still having issues, try generating a new App Password
• Make sure your Gmail account is not using advanced protection
        """
    
    def test_email_connection(self, email: str, password: str) -> Dict:
        """Test SMTP connection tanpa sending email"""
        try:
            provider = self.detect_email_provider(email)
            smtp_config = self.email_providers[provider]
            
            context = ssl.create_default_context()
            
            with smtplib.SMTP(smtp_config['smtp_server'], smtp_config['smtp_port']) as server:
                server.starttls(context=context)
                server.login(email, password)
            
            return {
                'success': True,
                'message': f'✅ Email connection successful! Provider: {provider.upper()}',
                'provider': provider
            }
            
        except smtplib.SMTPAuthenticationError:
            return {
                'success': False,
                'error': '❌ Authentication failed. Check email and password/App Password.'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'❌ Connection failed: {str(e)}'
            }

# =============================================
# STANDALONE FUNCTIONS FOR GUI COMPATIBILITY  
# =============================================

# Global instance
_email_sender = None

def _get_email_sender():
    """Get or create email sender instance"""
    global _email_sender
    if _email_sender is None:
        _email_sender = RealEmailSender()
    return _email_sender

def send_real_email(sender_email: str, sender_password: str, recipient_email: str,
                   stego_image_path: str, tx_hash: str, message_preview: str = "",
                   subject: str = None) -> Dict:
    """
    Standalone function untuk send real email - GUI compatible
    """
    try:
        email_sender = _get_email_sender()
        return email_sender.send_stego_email(
            sender_email=sender_email,
            sender_password=sender_password, 
            recipient_email=recipient_email,
            stego_image_path=stego_image_path,
            tx_hash=tx_hash,
            secret_message_preview=message_preview,
            subject=subject
        )
    except Exception as e:
        return {'success': False, 'error': f"Real email sending failed: {str(e)}"}

def validate_email_format(email: str) -> bool:
    """Validate email format - GUI compatible"""
    email_sender = _get_email_sender()
    return email_sender.validate_email(email)

def test_email_credentials(email: str, password: str) -> Dict:
    """Test email credentials - GUI compatible"""
    email_sender = _get_email_sender()
    return email_sender.test_email_connection(email, password)

def get_gmail_help() -> str:
    """Get Gmail App Password help - GUI compatible"""
    email_sender = _get_email_sender()
    return email_sender.get_gmail_app_password_guide()

def detect_email_provider(email: str) -> str:
    """Detect email provider - GUI compatible"""
    email_sender = _get_email_sender()
    return email_sender.detect_email_provider(email)