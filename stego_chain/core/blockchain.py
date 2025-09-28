from web3 import Web3
from stego_chain import config

# Inisialisasi koneksi
w3 = Web3(Web3.HTTPProvider(config.RPC_URL))

def check_connection():
    """Memeriksa apakah koneksi ke blockchain berhasil."""
    return w3.is_connected()

def send_transaction(recipient_address, hex_data):
    """Membangun, menandatangani, dan mengirim transaksi."""
    try:
        nonce = w3.eth.get_transaction_count(config.YOUR_ADDRESS)
        
        tx = {
            'nonce': nonce,
            'to': recipient_address,
            'value': w3.to_wei(0, 'ether'),
            'gas': 100000,
            'gasPrice': w3.eth.gas_price,
            'data': '0x' + hex_data
        }
        
        signed_tx = w3.eth.account.sign_transaction(tx, config.PRIVATE_KEY)
        
        # Fix untuk Web3 compatibility - coba kedua cara
        try:
            raw_tx = signed_tx.raw_transaction  # Web3 >= 6.0
        except AttributeError:
            raw_tx = signed_tx.rawTransaction   # Web3 < 6.0
        
        tx_hash = w3.eth.send_raw_transaction(raw_tx)
        
        print(f"✅ Transaksi berhasil dikirim!")
        print(f"Hash: {tx_hash.hex()}")
        print(f"Explorer: https://sepolia.etherscan.io/tx/{tx_hash.hex()}")
        
        return tx_hash.hex()
        
    except Exception as e:
        print(f"❌ Error blockchain: {str(e)}")
        raise e

def get_transaction_data(tx_hash):
    """Mengambil data dari sebuah transaksi berdasarkan hash-nya."""
    try:
        print(f"🔍 Mencari transaksi: {tx_hash}")
        
        # Pastikan format hash
        if not tx_hash.startswith('0x'):
            tx_hash = '0x' + tx_hash
            
        tx = w3.eth.get_transaction(tx_hash)
        
        if not tx.input or tx.input == '0x':
            raise ValueError("Transaksi tidak mengandung data tersembunyi")
        
        # Debug informasi
        print(f"📋 From: {tx['from']}")
        print(f"📋 To: {tx['to']}")
        print(f"📋 Value: {tx['value']} wei")
        print(f"📋 Input type: {type(tx.input)}")
        print(f"📋 Input raw: {str(tx.input)[:50]}...")
            
        # Ambil hex data
        if isinstance(tx.input, bytes):
            hex_data = tx.input.hex()
        else:
            hex_data = str(tx.input)
            
        if hex_data.startswith('0x'):
            hex_data = hex_data[2:]
        
        print(f"📦 Data ditemukan: {len(hex_data)} karakter hex")
        print(f"🔍 Preview: {hex_data[:32]}...")
        
        # Validasi data length (harus genap untuk hex)
        if len(hex_data) % 2 != 0:
            raise ValueError(f"Invalid hex data length: {len(hex_data)}")
            
        return hex_data
        
    except Exception as e:
        print(f"❌ Error saat mengambil data transaksi: {str(e)}")
        raise e