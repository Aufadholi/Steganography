from stego_chain.core.blockchain import check_connection
from stego_chain.utils.hybrid_integration import HybridSteganographyBlockchain
from stego_chain.utils.email_simulation import EmailSimulation, demo_inbox_check
from stego_chain import config
import os

print(f"🔗 Connecting to blockchain: {config.RPC_URL}")

def main():
    print("🚀 === HYBRID LSB STEGANOGRAPHY-BLOCKCHAIN SYSTEM ===")
    print("    Secure Digital Communication with Integrity Verification")
    print("=" * 60)
    
    if not check_connection():
        print("❌ Gagal terhubung ke blockchain. Periksa RPC_URL Anda.")
        return

    print("✅ Koneksi ke Blockchain Berhasil.")
    
    hybrid_system = HybridSteganographyBlockchain()
    email_sim = EmailSimulation()
    
    while True:
        print("\n📋 === MENU UTAMA ===")
        print("1. 📤 Send Secure Message (LSB + Blockchain)")
        print("2. 📥 Receive Secure Message (Extract + Verify)")
        print("3. 📧 Check Email Inbox (Simulation)")
        print("4. 🔍 Demo Mode (Full Workflow)")
        print("5. ❌ Keluar")
        
        choice = input("\nPilihan Anda (1-5): ").strip()
        
        if choice == '1':
            send_secure_message(hybrid_system, email_sim)
        elif choice == '2':
            receive_secure_message(hybrid_system, email_sim)
        elif choice == '3':
            check_email_inbox(email_sim)
        elif choice == '4':
            demo_full_workflow(hybrid_system, email_sim)
        elif choice == '5':
            print("📝 Terima kasih telah menggunakan Hybrid Steganography System!")
            break
        else:
            print("❌ Pilihan tidak valid. Silakan pilih 1-5.")

def send_secure_message(hybrid_system, email_sim):
    """Handle pengiriman pesan aman"""
    print("\n📤 === SEND SECURE MESSAGE ===")
    
    # Input parameters
    cover_image = input("📁 Path gambar cover (PNG/BMP): ").strip()
    if not os.path.exists(cover_image):
        print("❌ File gambar tidak ditemukan!")
        return
    
    secret_message = input("💬 Pesan rahasia: ").strip()
    if not secret_message:
        print("❌ Pesan tidak boleh kosong!")
        return
    
    recipient_address = input("📧 Alamat wallet penerima: ").strip()
    if not recipient_address.startswith('0x') or len(recipient_address) != 42:
        print("❌ Format alamat tidak valid!")
        return
    
    password = input("🔐 Password enkripsi (Enter untuk skip): ").strip()
    password = password if password else None
    
    # Execute hybrid sending
    result = hybrid_system.send_secure_message(
        cover_image, secret_message, recipient_address, password
    )
    
    if result['success']:
        print("\n🎉 Hybrid sending berhasil!")
        
        # Simulate email sending
        print("\n📧 Simulating email transfer...")
        email_result = email_sim.send_stego_email(
            "alice@example.com", "bob@example.com",
            result['stego_image_path'], result['blockchain_tx_hash'],
            "Confidential Document"
        )
        
        if email_result['success']:
            print(f"✅ Email simulation successful (ID: {email_result['email_id']})")
        
        print(f"\n📋 === SUMMARY ===")
        print(f"🖼️  Stego image: {os.path.basename(result['stego_image_path'])}")
        print(f"🔗 Blockchain TX: {result['blockchain_tx_hash']}")
        print(f"📊 PSNR: {result['embed_metrics']['psnr']:.2f} dB")
        print(f"📄 Report: {os.path.basename(result['report_path'])}")
        
    else:
        print(f"❌ Pengiriman gagal: {result['error']}")

def receive_secure_message(hybrid_system, email_sim):
    """Handle penerimaan dan verifikasi pesan"""
    print("\n📥 === RECEIVE SECURE MESSAGE ===")
    
    # Show available options
    print("Pilih sumber:")
    print("1. Manual input (path + tx hash)")
    print("2. From email inbox")
    
    source = input("Pilihan (1-2): ").strip()
    
    if source == '1':
        # Manual input
        stego_image = input("📁 Path gambar stego: ").strip()
        if not os.path.exists(stego_image):
            print("❌ File gambar tidak ditemukan!")
            return
        
        tx_hash = input("🔗 Transaction hash: ").strip()
        if not tx_hash.startswith('0x'):
            print("❌ Format transaction hash tidak valid!")
            return
        
    elif source == '2':
        # From email inbox
        messages = email_sim.get_inbox_messages("bob@example.com")
        if not messages:
            print("📭 Inbox kosong!")
            return
        
        print("\n📨 Available messages:")
        for i, msg in enumerate(messages[:5], 1):
            print(f"{i}. From: {msg['from']} | Subject: {msg['subject']}")
            print(f"   TX: {msg['blockchain_info']['tx_hash'][:16]}...")
        
        try:
            msg_idx = int(input("Pilih pesan (nomor): ")) - 1
            if 0 <= msg_idx < len(messages):
                email_data = email_sim.read_email(messages[msg_idx]['email_id'], "bob@example.com")
                if email_data['success']:
                    stego_image = email_data['stego_image_path']
                    tx_hash = email_data['tx_hash']
                    print(f"✅ Email selected: {messages[msg_idx]['subject']}")
                else:
                    print(f"❌ Error reading email: {email_data['error']}")
                    return
            else:
                print("❌ Nomor pesan tidak valid!")
                return
        except ValueError:
            print("❌ Input tidak valid!")
            return
    else:
        print("❌ Pilihan tidak valid!")
        return
    
    password = input("🔐 Password dekripsi (Enter untuk skip): ").strip()
    password = password if password else None
    
    # Execute hybrid receiving
    result = hybrid_system.receive_secure_message(stego_image, tx_hash, password)
    
    if result['success']:
        print(f"\n🎉 Message extraction berhasil!")
        print(f"📝 Pesan: '{result['message']}'")
        print(f"🔒 Integrity: {'✅ VERIFIED' if result['integrity_verified'] else '❌ UNVERIFIED'}")
        print(f"📄 Report: {os.path.basename(result['verification_report'])}")
    else:
        print(f"❌ Extraction gagal: {result['error']}")

def check_email_inbox(email_sim):
    """Check email inbox simulation"""
    print("\n📨 === EMAIL INBOX CHECK ===")
    demo_inbox_check("bob@example.com")

def demo_full_workflow(hybrid_system, email_sim):
    """Demo complete workflow dengan sample data"""
    print("\n🔍 === DEMO MODE: FULL WORKFLOW ===")
    print("Demo ini akan menggunakan sample image dan data untuk testing")
    
    # Create sample image jika tidak ada
    sample_image = "sample_cover.png"
    if not os.path.exists(sample_image):
        print("📁 Creating sample image...")
        from PIL import Image
        import numpy as np
        
        # Create simple 200x200 blue image
        img_array = np.full((200, 200, 3), [100, 150, 200], dtype=np.uint8)
        img = Image.fromarray(img_array)
        img.save(sample_image)
        print(f"✅ Sample image created: {sample_image}")
    
    # Demo parameters
    demo_message = "This is a confidential message for research purposes!"
    demo_recipient = "0x50E5786732143f349d55197388Db32d1b7DB8e5"  # Bob's address
    demo_password = "demo123"
    
    print(f"\n📋 Demo Parameters:")
    print(f"📁 Cover image: {sample_image}")
    print(f"💬 Message: '{demo_message}'")
    print(f"📧 Recipient: {demo_recipient}")
    print(f"🔐 Password: {demo_password}")
    
    confirm = input("\nProceed with demo? (y/n): ").strip().lower()
    if confirm != 'y':
        return
    
    # Execute demo workflow
    print("\n🚀 Starting demo workflow...")
    
    # Step 1: Send
    print("\n--- STEP 1: SENDING ---")
    send_result = hybrid_system.send_secure_message(
        sample_image, demo_message, demo_recipient, demo_password
    )
    
    if not send_result['success']:
        print(f"❌ Demo sending failed: {send_result['error']}")
        return
    
    # Step 2: Email simulation
    print("\n--- STEP 2: EMAIL TRANSFER ---")
    email_result = email_sim.send_stego_email(
        "alice@example.com", "bob@example.com",
        send_result['stego_image_path'], send_result['blockchain_tx_hash'],
        "Demo: Confidential Research Data"
    )
    
    # Step 3: Receive
    print("\n--- STEP 3: RECEIVING ---")
    receive_result = hybrid_system.receive_secure_message(
        send_result['stego_image_path'], send_result['blockchain_tx_hash'], demo_password
    )
    
    if receive_result['success']:
        print(f"\n🎉 === DEMO COMPLETED SUCCESSFULLY ===")
        print(f"📝 Original message: '{demo_message}'")
        print(f"📝 Extracted message: '{receive_result['message']}'")
        print(f"🔒 Integrity verified: {'✅ YES' if receive_result['integrity_verified'] else '❌ NO'}")
        print(f"📊 PSNR quality: {send_result['embed_metrics']['psnr']:.2f} dB")
        print(f"📧 Email ID: {email_result.get('email_id', 'N/A')}")
    else:
        print(f"❌ Demo receiving failed: {receive_result['error']}")

if __name__ == "__main__":
    main()