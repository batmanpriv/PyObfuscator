# 🛡️ PyObfuscator

**Advanced Python Code Obfuscation Tool**

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0-brightgreen.svg)]()

---

## 📌 Overview

**PyObfuscator** is a Python code obfuscation tool with 40+ obfuscation methods including AST-level transformation, multi-layer encryption, CJK junk injection, and military-grade protection.

> **Developer:** [@BatmanPriv](https://t.me/BatmanPriv) | [GitHub](https://github.com/batmanpriv)

---

## 📸 Screenshot

<img src="https://github.com/user-attachments/assets/036d7eb8-66d0-4d54-af9a-ce7f57ccf891">

---

## ⚡ Features

### 40+ Obfuscation Methods

| Method | Description |
|--------|-------------|
| **Marshal** | Python bytecode serialization |
| **Zlib / GZIP / LZMA** | Compression-based encoding |
| **Base16 / Base32 / Base64** | Encoding layers |
| **AST Control Flow Flattening** | Converts structured code to state-machine |
| **AST Variable Renaming** | Replaces identifiers with meaningless names |
| **AST String Encryption** | AES-256-CBC encrypted strings |
| **CJK Obfuscation** | Korean/Chinese/Japanese variable names + AST junk injection |
| **Ultra Obfuscation** | AES-256-GCM + ChaCha20 + Salsa20 + XOR quadruple-layer |

---

## 🧠 Obfuscation Mechanisms

### 1. AST-Level Transformation (Option 43)

Operates directly on Python's Abstract Syntax Tree:

- **Control Flow Flattening**: Converts structured code into a flat state-machine representation, making logical flow analysis extremely difficult for both humans and automated tools.

- **Variable Renaming**: Replaces meaningful variable names with meaningless identifiers.

- **String Encryption**: Encrypts all string literals with AES-256-CBC using per-string initialization vectors and decrypts them at runtime.

### 2. Dead Code Injection with CJK (Option 44)

Injects hundreds/thousands of lines of garbage code with Korean/Chinese/Japanese variable names:

```python
홁 = [2847 for _ in range(45)]
鰿 = {(lambda 鍘: 鍘 ^ 127)(i) for i in range(30)}
桽 = [(lambda 鼜, 鰪: 鼜 * 鰪)(i, j) for i in range(67) for j in range(7)]
```
These characters are visually confusing and cause decompilers to fail.

### 3. Multi-Layer Encryption Pipeline (Option 44)

```
Original Code
    ↓
AST Transformation (Flatten + Rename + Encrypt Strings)
    ↓
Marshal Serialization
    ↓
Zlib Compression (Level 9)
    ↓
Zlib Compression (Level 9) - Second Pass
    ↓
BZ2 Compression
    ↓
LZMA Compression
    ↓
Base85 Encoding
    ↓
XOR-32 Encryption (32-byte random key)
    ↓
Shuffle Encryption (random permutation)
    ↓
RC4 Encryption (16-byte random key)
    ↓
LCG-XOR Encryption (Linear Congruential Generator)
    ↓
Base64 Encoding
    ↓
Final Protected Code
```

**Why This Pipeline Is Effective:**
- Each layer uses different algorithms, preventing single-point decryption
- The shuffle layer breaks pattern recognition
- LCG-XOR creates pseudo-random output that resists statistical analysis
- Compression before encryption removes redundancy

### 4. Ultra Obfuscation (Option 45)

Quadruple-layer encryption:

**Layer 1: AES-256-GCM**
- 256-bit key strength
- Authenticated encryption with integrity verification
- 96-bit nonce for uniqueness

**Layer 2: ChaCha20 Stream Cipher**
- 256-bit key
- 96-bit nonce
- Designed for high performance in software

**Layer 3: Salsa20 Stream Cipher**
- 256-bit key
- 64-bit nonce
- Additional layer of confusion

**Layer 4: XOR with 256-byte Key**
- 256-byte XOR key
- Added complexity layer

**Key Derivation:**
All keys are derived using **scrypt** with:
- N=65536 (2^16)
- r=8
- p=1
- 64-byte master entropy

This makes brute-force attacks computationally infeasible.

### 5. Deep XOR Obfuscation (Option 42)

Combines XOR encryption with multiple protection mechanisms:

## 🚀 Installation

```bash
git clone https://github.com/batmanpriv/PyObfuscator.git
cd PyObfuscator
python PyObfuscator.py
```

Auto-installs: `pip install pycryptodome`

---

## 📖 Usage

```bash
python PyObfuscator.py
```

### Menu

```
[1]  Marshal Encode
[2]  Zlib Encode
[3]  Base16 Encode
[4]  Base32 Encode
[5]  Base64 Encode
[6]  LZMA Encode
[7]  GZIP Encode
[8]  Zlib + Base16
[9]  Zlib + Base32
[10] Zlib + Base64
[11] GZIP + Base16
[12] GZIP + Base32
[13] GZIP + Base64
[14] LZMA + Base16
[15] LZMA + Base32
[16] LZMA + Base64
[17] Marshal + Zlib
[18] Marshal + GZIP
[19] Marshal + LZMA
[20] Marshal + Base16
[21] Marshal + Base32
[22] Marshal + Base64
[23] Marshal + Zlib + Base16
[24] Marshal + Zlib + Base32
[25] Marshal + Zlib + Base64
[26] Marshal + LZMA + Base16
[27] Marshal + LZMA + Base32
[28] Marshal + LZMA + Base64
[29] Marshal + GZIP + Base16
[30] Marshal + GZIP + Base32
[31] Marshal + GZIP + Base64
[32] Marshal + Zlib + LZMA + Base16
[33] Marshal + Zlib + LZMA + Base32
[34] Marshal + Zlib + LZMA + Base64
[35] Marshal + Zlib + GZIP + Base16
[36] Marshal + Zlib + GZIP + Base32
[37] Marshal + Zlib + GZIP + Base64
[38] Marshal + Zlib + LZMA + GZIP + Base16
[39] Marshal + Zlib + LZMA + GZIP + Base32
[40] Marshal + Zlib + LZMA + GZIP + Base64
[41] Simple Obfuscation
[42] Deep XOR Obfuscation
[43] AST Obfuscation (Control Flow + Strings)
[44] AST Obfuscation (CJK + Junk + Multi-layer)
[45] Ultra Obfuscation (AES+ChaCha20+Salsa20+XOR)
[46] Exit
```

### Example

```bash
$ python PyObfuscator.py
[+] Option: 45
[+] File Name: my_script.py
[+] Obfuscation complete: my_script.py
[+] Output: my_script_ultra.py
[+] Size: 184.3 KB
```

---

## 📊 Performance & Effectiveness

| Method | Size Expansion | Speed | Protection Level |
|--------|---------------|-------|------------------|
| Options 1-7 | 1.5x | <1s | Low |
| Options 8-16 | 2x | <2s | Medium |
| Options 17-40 | 3-5x | 2-5s | High |
| Option 41 | 2x | <2s | Medium |
| Option 42 | 5-8x | 3-7s | Very High |
| Option 43 | 8-12x | 4-8s | High |
| Option 44 | 15-30x | 5-10s | Extreme |
| Option 45 | 10-20x | 3-6s | Military-Grade |

**Automated Decryption Success Rate:**
- Options 1-40: >60%
- Option 41: >40%
- Option 42: <15%
- Option 43: <10%
- Option 44: <5%
- Option 45: <0.1%

---

## 🔧 Technical Specifications

**Supported Python Versions:**
- Python 3.6 → 3.13

**Dependencies:**
```
pycryptodome >= 3.15.0
```

**File Size Limits:**
- Input: Unlimited
- Output: Varies by method (10KB - 50MB)

**Memory Usage:**
- Options 1-40: <100MB
- Options 41-43: <200MB
- Options 44-45: <500MB

---

## 🎯 When To Use Each Method

| Method | Best For |
|--------|----------|
| 1-7 | Quick basic protection, learning purposes |
| 8-16 | Moderate protection, when size expansion is a concern |
| 17-40 | Commercial software, API keys protection |
| 41 | Quick moderate security |
| 43 | Deep structural obfuscation, professional software |
| 44 | Maximum confusion, protection against decompilers |
| 45 | Military-grade protection |
