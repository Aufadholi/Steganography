# 🔐 Stego-Chain: Blockchain Steganography Application

## 📝 Deskripsi
Aplikasi steganografi berbasis blockchain yang menggunakan teknologi Ethereum untuk menyembunyikan pesan rahasia dalam transaksi blockchain dengan keamanan berlapis.

## 🎯 Fitur Utama
- **🔒 Steganografi**: Menyembunyikan pesan dalam transaksi blockchain
- **🔐 Enkripsi**: Enkripsi AES dengan kunci rahasia
- **📦 Kompresi**: Kompresi data untuk efisiensi
- **🌐 Blockchain**: Penyimpanan immutable di Ethereum Sepolia
- **🔍 Verifikasi**: Tracking transaksi melalui block explorer

## ⚡ Cara Penggunaan

### 1. Kirim Pesan Rahasia
```
1. Pilih menu "Kirim Pesan Rahasia"
2. Masukkan alamat wallet penerima
3. Ketik pesan rahasia Anda
4. Buat kunci rahasia (shared secret)
5. Simpan hash transaksi yang dihasilkan
```

### 2. Baca Pesan Rahasia
```
1. Pilih menu "Baca Pesan Rahasia"
2. Masukkan hash transaksi
3. Masukkan kunci rahasia yang sama
4. Pesan akan diekstrak dan ditampilkan
```

## 🛠️ Instalasi
```bash
# Clone repository
git clone [repository-url]

# Masuk ke direktori
cd stego-chain

# Aktivasi virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
# Edit file .env dengan kredensial Ethereum Anda
```

## 📋 Requirements
- Python 3.8+
- Web3.py
- PyCryptodome
- Python-dotenv
- MetaMask wallet dengan Sepolia testnet

## 🔧 Konfigurasi
Edit file `.env`:
```
PRIVATE_KEY="your_private_key"
RPC_URL="https://sepolia.infura.io/v3/your_project_id"
YOUR_ADDRESS="your_ethereum_address"
```

## 🎯 Use Cases
- **Komunikasi Rahasia**: Mengirim pesan tersembunyi
- **Digital Watermarking**: Proof of ownership
- **Secure Documentation**: Penyimpanan dokumen terenkripsi
- **Research Purpose**: Studi steganografi blockchain

## 🔒 Keamanan
- **Double Layer**: Steganografi + Enkripsi
- **Blockchain Immutability**: Data tidak dapat diubah
- **Decentralized**: Tidak bergantung server terpusat
- **Cryptographic**: Menggunakan algoritma standar industri

## 📊 Arsitektur
```
User Input → Compression → Encryption → Blockchain Transaction
                                                    ↓
Block Explorer ← Extract Data ← Decryption ← Decompression
```

## 👥 Target Pengguna
- Peneliti Blockchain
- Security Engineer  
- Crypto Enthusiast
- Academic Research

## 📜 Lisensi
Educational & Research Purpose

## 🤝 Kontributor
- Mahasiswa TA Informatika
- Supervisor: 

---
**⚠️ Disclaimer**: Aplikasi ini untuk tujuan edukasi dan penelitian. Gunakan dengan bertanggung jawab.
