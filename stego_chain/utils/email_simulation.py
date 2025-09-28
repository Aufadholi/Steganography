"""
Email Simulation System untuk Dual-Channel Testing
Simulasi pengiriman file stego dan penerimaan untuk testing
"""

import os
import json
import shutil
from datetime import datetime
from typing import Dict, List
import uuid

class EmailSimulation:
    """Simulasi sistem email untuk testing dual-channel steganography"""
    
    def __init__(self):
        self.inbox_dir = "simulation/inbox"
        self.sent_dir = "simulation/sent"  
        self.accounts_file = "simulation/accounts.json"
        self._setup_simulation()
    
    def _setup_simulation(self):
        """Setup direktori dan akun simulasi"""
        # Buat direktori
        os.makedirs(self.inbox_dir, exist_ok=True)
        os.makedirs(self.sent_dir, exist_ok=True)
        os.makedirs("simulation", exist_ok=True)
        
        # Setup akun email contoh
        if not os.path.exists(self.accounts_file):
            accounts = {
                "alice@example.com": {
                    "name": "Alice Sender",
                    "metamask_address": "0x03C779967c8581e092570e5d77832dFF7cF9ae27",
                    "role": "sender"
                },
                "bob@example.com": {
                    "name": "Bob Receiver", 
                    "metamask_address": "0x50E57867322143f349d55197388Db32d1b7DB8e5",
                    "role": "receiver"
                }
            }
            
            with open(self.accounts_file, 'w') as f:
                json.dump(accounts, f, indent=2)
            
            print("📧 Email simulation accounts created:")
            print("   - alice@example.com (Sender)")
            print("   - bob@example.com (Receiver)")
    
    def send_stego_email(self, sender_email: str, recipient_email: str, 
                        stego_image_path: str, tx_hash: str, subject: str = None) -> Dict:
        """
        Simulasi pengiriman email dengan stego image
        
        Args:
            sender_email: Email pengirim
            recipient_email: Email penerima
            stego_image_path: Path gambar stego
            tx_hash: Hash transaksi blockchain
            subject: Subject email (optional)
            
        Returns:
            Dict hasil pengiriman
        """
        try:
            # Load akun
            with open(self.accounts_file, 'r') as f:
                accounts = json.load(f)
            
            if sender_email not in accounts or recipient_email not in accounts:
                return {'success': False, 'error': 'Email account not found'}
            
            # Generate email ID
            email_id = str(uuid.uuid4())[:8]
            timestamp = datetime.now()
            
            # Copy stego image ke sent folder
            sent_image_name = f"stego_{email_id}_{os.path.basename(stego_image_path)}"
            sent_image_path = os.path.join(self.sent_dir, sent_image_name)
            shutil.copy2(stego_image_path, sent_image_path)
            
            # Create email metadata
            email_data = {
                'email_id': email_id,
                'from': sender_email,
                'to': recipient_email,
                'subject': subject or f"Secure Document #{email_id}",
                'timestamp': timestamp.isoformat(),
                'attachments': [
                    {
                        'filename': os.path.basename(stego_image_path),
                        'filepath': sent_image_name,
                        'size': os.path.getsize(stego_image_path),
                        'type': 'stego_image'
                    }
                ],
                'blockchain_info': {
                    'tx_hash': tx_hash,
                    'sender_address': accounts[sender_email]['metamask_address'],
                    'recipient_address': accounts[recipient_email]['metamask_address']
                },
                'body': f"""
Secure document has been sent via hybrid steganography system.

Instructions:
1. Download the attached image
2. Check your MetaMask for transaction: {tx_hash}
3. Use the steganography extraction tool
4. Verify integrity via blockchain

This message was sent securely using LSB steganography with blockchain verification.

Regards,
{accounts[sender_email]['name']}
                """.strip()
            }
            
            # Save ke sent folder
            sent_metadata = os.path.join(self.sent_dir, f"email_{email_id}.json")
            with open(sent_metadata, 'w') as f:
                json.dump(email_data, f, indent=2)
            
            # Deliver ke inbox
            self._deliver_to_inbox(email_data, sent_image_path)
            
            print(f"📧 Email sent successfully!")
            print(f"   From: {sender_email}")
            print(f"   To: {recipient_email}")
            print(f"   Subject: {email_data['subject']}")
            print(f"   Attachment: {os.path.basename(stego_image_path)}")
            print(f"   Email ID: {email_id}")
            
            return {
                'success': True,
                'email_id': email_id,
                'sent_metadata': sent_metadata,
                'sent_image': sent_image_path
            }
            
        except Exception as e:
            print(f"❌ Email sending error: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _deliver_to_inbox(self, email_data: Dict, image_path: str):
        """Deliver email ke inbox penerima"""
        # Copy image ke inbox
        inbox_image_name = f"received_{email_data['email_id']}_{os.path.basename(image_path)}"
        inbox_image_path = os.path.join(self.inbox_dir, inbox_image_name)
        shutil.copy2(image_path, inbox_image_path)
        
        # Update attachment path untuk inbox
        email_data['attachments'][0]['filepath'] = inbox_image_name
        email_data['status'] = 'delivered'
        email_data['delivery_time'] = datetime.now().isoformat()
        
        # Save ke inbox
        inbox_metadata = os.path.join(self.inbox_dir, f"email_{email_data['email_id']}.json")
        with open(inbox_metadata, 'w') as f:
            json.dump(email_data, f, indent=2)
    
    def get_inbox_messages(self, recipient_email: str) -> List[Dict]:
        """Get semua pesan di inbox untuk recipient"""
        try:
            messages = []
            
            # Load akun
            with open(self.accounts_file, 'r') as f:
                accounts = json.load(f)
            
            if recipient_email not in accounts:
                return []
            
            # Scan inbox folder
            for filename in os.listdir(self.inbox_dir):
                if filename.startswith('email_') and filename.endswith('.json'):
                    filepath = os.path.join(self.inbox_dir, filename)
                    
                    with open(filepath, 'r') as f:
                        email_data = json.load(f)
                    
                    # Filter by recipient
                    if email_data['to'] == recipient_email:
                        messages.append(email_data)
            
            # Sort by timestamp (newest first)
            messages.sort(key=lambda x: x['timestamp'], reverse=True)
            
            return messages
            
        except Exception as e:
            print(f"❌ Error reading inbox: {str(e)}")
            return []
    
    def read_email(self, email_id: str, recipient_email: str) -> Dict:
        """Read specific email dan return stego image path"""
        try:
            messages = self.get_inbox_messages(recipient_email)
            
            for message in messages:
                if message['email_id'] == email_id:
                    # Get attachment path
                    if message['attachments']:
                        attachment = message['attachments'][0]
                        image_path = os.path.join(self.inbox_dir, attachment['filepath'])
                        
                        if os.path.exists(image_path):
                            return {
                                'success': True,
                                'email_data': message,
                                'stego_image_path': image_path,
                                'tx_hash': message['blockchain_info']['tx_hash']
                            }
                        else:
                            return {'success': False, 'error': 'Attachment file not found'}
                    else:
                        return {'success': False, 'error': 'No attachments found'}
            
            return {'success': False, 'error': 'Email not found'}
            
        except Exception as e:
            print(f"❌ Error reading email: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def show_inbox(self, recipient_email: str):
        """Display inbox untuk recipient"""
        print(f"\n📨 === INBOX for {recipient_email} ===")
        
        messages = self.get_inbox_messages(recipient_email)
        
        if not messages:
            print("📭 No messages in inbox")
            return
        
        for i, msg in enumerate(messages, 1):
            print(f"\n{i}. Email ID: {msg['email_id']}")
            print(f"   From: {msg['from']}")
            print(f"   Subject: {msg['subject']}")
            print(f"   Date: {msg['timestamp'][:19].replace('T', ' ')}")
            print(f"   Attachments: {len(msg['attachments'])}")
            if msg['attachments']:
                att = msg['attachments'][0]
                print(f"   - {att['filename']} ({att['size']} bytes)")
            print(f"   Blockchain TX: {msg['blockchain_info']['tx_hash'][:16]}...")
    
    def get_account_info(self, email: str) -> Dict:
        """Get info akun email"""
        try:
            with open(self.accounts_file, 'r') as f:
                accounts = json.load(f)
            
            return accounts.get(email, {})
            
        except Exception as e:
            return {'error': str(e)}
    
    def list_accounts(self) -> Dict:
        """List semua akun yang tersedia"""
        try:
            with open(self.accounts_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            return {'error': str(e)}

# Utility functions
def simulate_dual_channel_transfer(stego_image_path: str, tx_hash: str, 
                                 sender_email: str = "alice@example.com",
                                 recipient_email: str = "bob@example.com") -> Dict:
    """
    Utility function untuk simulasi complete dual-channel transfer
    """
    email_sim = EmailSimulation()
    
    print("📧 Simulating dual-channel transfer...")
    print(f"   Channel 1: Email ({sender_email} → {recipient_email})")
    print(f"   Channel 2: Blockchain (TX: {tx_hash[:16]}...)")
    
    # Send via email simulation
    result = email_sim.send_stego_email(
        sender_email, recipient_email, stego_image_path, tx_hash,
        subject="Confidential Document - Secure Transfer"
    )
    
    return result

def demo_inbox_check(recipient_email: str = "bob@example.com"):
    """Demo function untuk cek inbox"""
    email_sim = EmailSimulation()
    email_sim.show_inbox(recipient_email)
    return email_sim.get_inbox_messages(recipient_email)

# =============================================
# STANDALONE FUNCTIONS FOR GUI COMPATIBILITY
# =============================================

# Global instance for standalone functions
_email_sim = None

def _get_email_sim():
    """Get or create email simulation instance"""
    global _email_sim
    if _email_sim is None:
        _email_sim = EmailSimulation()
    return _email_sim

def send_stego_email(sender_email: str, recipient_email: str, stego_image_path: str, 
                    tx_hash: str, subject: str = "Secure Transfer") -> Dict:
    """
    Standalone function untuk GUI compatibility
    Send stego email using email simulation system
    """
    try:
        email_sim = _get_email_sim()
        return email_sim.send_stego_email(sender_email, recipient_email, 
                                         stego_image_path, tx_hash, subject)
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_inbox_messages(recipient_email: str) -> List[Dict]:
    """
    Standalone function untuk GUI compatibility
    Get inbox messages for recipient
    """
    try:
        email_sim = _get_email_sim()
        return email_sim.get_inbox_messages(recipient_email)
    except Exception as e:
        return []