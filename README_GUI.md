# 🖥️ GUI User Manual - Hybrid LSB Steganography-Blockchain System

## 🚀 Quick Start

### Cara Menjalankan GUI:
```bash
# Method 1: Direct launch (Recommended)
python launch_gui.py

# Method 2: Direct GUI script
python gui_steganography.py
```

### Requirements:
- Python 3.8+
- tkinter (included with Python on Windows)
- All dependencies in `requirements.txt`

---

## 📱 Interface Overview

### 🎯 Tab Navigation
GUI memiliki 3 tab utama:

1. **📤 Send Secret Message** - Embed pesan dalam gambar + blockchain
2. **📥 Receive Secret Message** - Extract dan verify pesan tersembunyi  
3. **🧪 Demo Workflow** - Complete end-to-end testing

---

## 📤 Send Secret Message Tab

### Step-by-Step Usage:

#### 1. **Select Cover Image** 📁
- Click **"Browse 📁"** button
- Pilih gambar PNG, JPG, BMP, atau TIFF
- Image akan ditampilkan di preview panel
- **Supported formats**: PNG (best), BMP, JPG, TIFF

#### 2. **Enter Secret Message** ✍️
- Type pesan rahasia di text area
- **Maximum capacity**: Depends on image size
  - 100x100 pixels ≈ 1,250 characters
  - 500x500 pixels ≈ 31,250 characters
  - 1000x1000 pixels ≈ 125,000 characters

#### 3. **Recipient Address** 🎯
- Enter Ethereum wallet address (0x...)
- Default: `0x50E5786732143f349d55197388Db32d1b7DB8e5`
- **Must be valid Ethereum address**

#### 4. **Send Message** 🚀
- Click **"🚀 Send Secret Message"**
- Progress bar akan show processing status
- **Output files created**:
  - `stego_output.png` - Image dengan pesan tersembunyi
  - Transaction hash untuk blockchain verification

### 📊 Results Display:
```
✅ MESSAGE SENT SUCCESSFULLY!
🔗 Transaction Hash: 0x1234abcd...
💾 Stego Image: stego_output.png

📊 QUALITY METRICS:
PSNR: 42.15 dB    ← Higher is better (>30 dB excellent)
MSE: 3.94         ← Lower is better (<10 excellent)  
Processing Time: 2.1s
```

---

## 📥 Receive Secret Message Tab

### Step-by-Step Usage:

#### 1. **Select Stego Image** 📁
- Click **"Browse 📁"** 
- Pilih image yang mengandung pesan tersembunyi
- Usually file dengan nama `stego_*.png`

#### 2. **Transaction Hash** (Optional) 🔗  
- Enter blockchain transaction hash untuk verification
- Format: `0x1234abcd...` atau `1234abcd...`
- **Jika kosong**: Extract tanpa blockchain verification

#### 3. **Extract & Verify** 🔍
- Click **"🔍 Extract & Verify Message"**
- Wait for processing completion

### 📝 Results Display:
```
✅ MESSAGE EXTRACTED SUCCESSFULLY!
📝 Message: Your secret message appears here
✅ BLOCKCHAIN VERIFICATION: PASSED
```

---

## 🧪 Demo Workflow Tab

### Automatic Testing:
- Click **"🚀 Run Complete Demo"**
- System will automatically:
  1. Create demo cover image
  2. Embed test message using LSB
  3. Send hash to blockchain  
  4. Extract and verify message
  5. Display research metrics

### Expected Output:
```
🎯 STARTING COMPLETE DEMO WORKFLOW
==================================================
📁 Creating demo cover image...
✅ Demo image created: demo_cover.png
📝 Test message: 🔒 DEMO: This is a secret research message...
📤 Recipient: 0x50E5786732143f349d55197388Db32d1b7DB8e5

🚀 PHASE 1: Sending secure message...
✅ Phase 1 SUCCESS!
🔗 TX Hash: 0xabc123...
📊 PSNR: 41.23 dB
📊 MSE: 4.56

🔍 PHASE 2: Extracting message...
✅ Phase 2 SUCCESS!
📝 Extracted: 🔒 DEMO: This is a secret research message...
🔒 Verified: YES

📊 DEMO COMPLETE - RESEARCH RESULTS:
==================================================
✅ Message integrity: PERFECT MATCH
✅ Blockchain verification: PASSED
✅ Image quality maintained: PSNR 41.23 dB
✅ Demo workflow: COMPLETED SUCCESSFULLY

🎯 Ready for Sinta 3+ research publication!
```

---

## 🔧 Troubleshooting

### Common Issues:

#### ❌ "No module named stego_chain"
```bash
# Solution: Run from correct directory
cd "d:\Semester 7\TA1\SteganoTA\stego-chain"
python launch_gui.py
```

#### ❌ "Please select a cover image"
- Make sure you clicked **Browse** button
- Check file path is shown in text field
- Try different image format (PNG recommended)

#### ❌ "Blockchain connection: FAILED"  
- Check internet connection
- Verify RPC_URL in `stego_chain/config.py`
- Make sure MetaMask accounts are configured

#### ❌ "Invalid hex data length"
- Try different transaction hash
- Make sure hash format is correct (0x...)
- Check if transaction contains data

#### ⚠️ Low PSNR Values (<30 dB)
- Use PNG format instead of JPG
- Try smaller message
- Use higher resolution image

### 🖼️ Image Format Guidelines:

#### ✅ **Recommended: PNG**
- Lossless compression
- Perfect for steganography
- Best PSNR results

#### ⚠️ **Caution: JPG/JPEG**
- Lossy compression may affect hidden data
- Lower PSNR values
- Use only for testing

#### ✅ **Good: BMP**  
- Uncompressed format
- Large file sizes
- Excellent for research

---

## 📊 Research Data Collection

### Quality Metrics Interpretation:

#### **PSNR (Peak Signal-to-Noise Ratio)**
- **>40 dB**: Excellent quality (imperceptible)
- **30-40 dB**: Good quality (minimal distortion)
- **<30 dB**: Noticeable distortion

#### **MSE (Mean Squared Error)**  
- **<5**: Excellent (minimal error)
- **5-15**: Good quality
- **>15**: Noticeable artifacts

### 📈 For Academic Paper:
1. **Run multiple tests** with different image sizes
2. **Record metrics** for statistical analysis
3. **Compare formats** (PNG vs BMP vs JPG)
4. **Test message lengths** vs quality impact
5. **Measure processing times** for performance analysis

---

## 🎯 Tips untuk Penelitian

### Best Practices:
1. **Use PNG images** for consistent results
2. **Test various message lengths** (100, 1000, 10000 chars)
3. **Document all metrics** for journal publication  
4. **Save output files** for evidence
5. **Test blockchain verification** with different accounts

### Sample Test Cases:
```
Test 1: Small message (100 chars) + 512x512 PNG
Test 2: Medium message (1000 chars) + 1024x1024 PNG  
Test 3: Large message (5000 chars) + high-res image
Test 4: Compare PNG vs BMP vs JPG quality
Test 5: Blockchain verification with different wallets
```

---

## 💡 Advanced Features

### Batch Processing (Future):
- Process multiple images
- Bulk message embedding
- Statistical analysis tools

### Security Enhancements:
- Message encryption before embedding
- Multi-layer steganography
- Advanced verification methods

---

**🔐 Ready to conduct world-class steganography research with blockchain integrity!** 

For technical support, check console output or contact research team.