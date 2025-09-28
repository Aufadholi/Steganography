from stego_chain.core import blockchain
from stego_chain.utils import compression, encryption

def embed_message(recipient_address, message, key):
    """Mengorkestrasi seluruh proses penyisipan pesan."""
    print("--- Memulai Proses Embedding ---")
    # 1. Kompresi
    compressed_data = compression.compress(message.encode('utf-8'))
    # 2. Enkripsi
    encrypted_data = encryption.encrypt(compressed_data, key)
    # 3. Konversi ke Hex
    hex_data = encrypted_data.hex()
    # 4. Kirim ke Blockchain
    tx_hash = blockchain.send_transaction(recipient_address, hex_data)
    print("--- Proses Embedding Selesai ---")
    return tx_hash

def extract_message(tx_hash, key):
    """Mengorkestrasi seluruh proses ekstraksi pesan."""
    print("--- Memulai Proses Ekstraksi ---")
    # 1. Ambil data dari Blockchain
    hex_data = blockchain.get_transaction_data(tx_hash)
    binary_data = bytes.fromhex(hex_data)
    # 2. Dekripsi
    decrypted_data = encryption.decrypt(binary_data, key)
    # 3. Dekompresi
    original_data = compression.decompress(decrypted_data)
    message = original_data.decode('utf-8')
    print("--- Proses Ekstraksi Selesai ---")
    return message