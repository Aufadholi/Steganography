from stego_chain.core import steganography
from stego_chain.core.blockchain import check_connection
from stego_chain import config
print(f"Mencoba terhubung dengan URL: {config.RPC_URL}")

def send_secret_message():
    """Menu untuk mengirim pesan rahasia"""
    print("\n=== KIRIM PESAN RAHASIA ===")
    recipient = input("📤 Masukkan alamat wallet penerima: ")
    message = input("💬 Masukkan pesan rahasia Anda: ")
    key = input("🔑 Masukkan kunci rahasia (shared secret): ")
    
    try:
        print("\n🔄 Memproses...")
        tx_hash = steganography.embed_message(recipient, message, key)
        print(f"\n✅ PESAN BERHASIL DIKIRIM!")
        print(f"📋 Hash Transaksi: {tx_hash}")
        print(f"🔗 Explorer: https://sepolia.etherscan.io/tx/{tx_hash}")
        print(f"\n💡 Berikan hash ini dan kunci '{key}' kepada penerima")
        return tx_hash
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def read_secret_message():
    """Menu untuk membaca pesan rahasia"""
    print("\n=== BACA PESAN TERSEMBUNYI ===")
    tx_hash = input("📋 Masukkan Hash Transaksi: ")
    key = input("🔑 Masukkan kunci rahasia (shared secret): ")
    
    try:
        print("\n🔄 Mengekstrak pesan...")
        message = steganography.extract_message(tx_hash, key)
        print(f"\n✅ PESAN BERHASIL DIEKSTRAK!")
        print(f"📩 Pesan: '{message}'")
        print(f"🔗 Verifikasi: https://sepolia.etherscan.io/tx/{tx_hash}")
        return message
    except Exception as e:
        print(f"❌ Gagal membaca pesan!")
        print(f"💡 Pastikan hash transaksi dan kunci benar")
        print(f"🔍 Error detail: {e}")
        return None

def main():
    print("🔐 ========== STEGO-CHAIN APPLICATION ==========")
    print("📱 Aplikasi Steganografi Blockchain Ethereum")
    print("=" * 50)
    
    if not check_connection():
        print("❌ Gagal terhubung ke blockchain. Periksa RPC_URL Anda.")
        return

    print("✅ Koneksi ke Blockchain Sepolia Berhasil!")
    
    while True:
        print(f"\n{'='*30}")
        print("🎯 MENU UTAMA:")
        print("1. 📤 Kirim Pesan Rahasia")
        print("2. 📥 Baca Pesan Rahasia")
        print("3. ℹ️  Informasi Aplikasi")
        print("4. 🚪 Keluar")
        print("="*30)
        
        choice = input("🎯 Pilihan Anda (1-4): ")
        
        if choice == '1':
            send_secret_message()
            
        elif choice == '2':
            read_secret_message()
            
        elif choice == '3':
            print(f"\n{'='*40}")
            print("ℹ️  INFORMASI APLIKASI")
            print("="*40)
            print("🔐 Nama: Stego-Chain")
            print("📝 Fungsi: Steganografi + Blockchain")
            print("🌐 Network: Ethereum Sepolia Testnet")
            print("🔒 Security: Compression + Encryption")
            print("📍 Address: " + config.YOUR_ADDRESS)
            print("="*40)
            
        elif choice == '4':
            print("\n👋 Terima kasih telah menggunakan Stego-Chain!")
            print("🔐 Stay secure!")
            break
            
        else:
            print("❌ Pilihan tidak valid. Silakan pilih 1-4.")

if __name__ == "__main__":
    main()