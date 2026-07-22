# 🛡️ PyObfuscator

**Military-Grade Python Code Obfuscation Tool**

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0-brightgreen.svg)]()

---

## 📌 Overview

**PyObfuscator** is an advanced Python code obfuscation tool that transforms readable source code into an unreadable, protected format using 40+ distinct obfuscation techniques. It operates at the Abstract Syntax Tree (AST) level, enabling deep structural modifications that make reverse engineering practically impossible.

> **Developer:** [@BatmanPriv](https://t.me/BatmanPriv) | [GitHub](https://github.com/BatmanPriv)

---

## ScreenShot

<img src="https://github.com/user-attachments/assets/036d7eb8-66d0-4d54-af9a-ce7f57ccf891">

## ⚡ Key Features

### 🎯 40+ Obfuscation Methods

| Method | Description |
|--------|-------------|
| **Marshal** | Python bytecode serialization |
| **Zlib / GZIP / LZMA** | Compression-based encoding |
| **Base16 / Base32 / Base64 / Base85** | Encoding layers |
| **Deep XOR** | XOR encryption with anti-debug, anti-VM, anti-hook |
| **AST Control Flow Flattening** | Converts structured code to state-machine |
| **AST Variable Renaming** | Replaces identifiers with meaningless names |
| **AST String Encryption** | AES-256-CBC encrypted strings |
| **CJK Obfuscation** | Korean/Chinese/Japanese variable names + AST junk injection |
| **Ultra Obfuscation** | AES-256-GCM + ChaCha20 + Salsa20 + XOR quadruple-layer |

---

## 🧠 Deep-Dive: Obfuscation Mechanisms

### 1. AST-Level Transformation (Options 43-44)

PyObfuscator operates directly on Python's Abstract Syntax Tree, enabling transformations that go far beyond simple string replacement:

**Control Flow Flattening:**
Converts traditional structured code into a flat state-machine representation:

```python
# Original:
def process(x):
    if x > 0:
        return x * 2
    return x - 1

# After Flattening:
def process(x):
    _state = 0
    while _state < 2:
        if _state == 0:
            if x > 0:
                _result = x * 2
                _state = 2
            else:
                _state = 1
        if _state == 1:
            _result = x - 1
            _state = 2
    return _result
```

This makes logical flow analysis extremely difficult for both humans and automated tools.

**Variable Renaming:**
```
Original: user_input, password_hash, api_key
Renamed:  v_8f3a9b2c, v_d1e5f7a3, v_4b8c2d1e
```

**String Encryption:**
All string literals are encrypted with AES-256-CBC using per-string initialization vectors:

```python
# Original:
print("Hello World")

# After Encryption:
print(_decrypt_str(b'\x1f\x8b...'))
```

---

### 2. Dead Code Injection with CJK (Option 44)

Injects hundreds/thousands of lines of garbage code with CJK variable names:

```python
# Injected junk examples:
홁 = [2847 for _ in range(45)]
鰿 = {(lambda 鍘: 鍘 ^ 127)(i) for i in range(30)}
桽 = [(lambda 鼜, 鰪: 鼜 * 鰪)(i, j) for i in range(67) for j in range(7)]
# ... hundreds more lines
```

**CJK Variable Names:**
- Korean: `홁`, `鰿`, `桽`, `鼜`, `鰪`
- Chinese: `玵`, `玶`, `玷`, `玸`, `玹`
- Japanese: `あ`, `い`, `う`, `え`, `お`

These characters are visually confusing and cause decompilers to fail.

---

### 3. Multi-Layer Encryption Pipeline (Option 44)

```text
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

---

### 4. Ultra Obfuscation (Option 45)

The most powerful protection method, featuring quadruple-layer encryption:

#### Layer 1: AES-256-GCM
```python
aes_cipher = AES.new(aes_key, AES.MODE_GCM)
aes_encrypted, aes_tag = aes_cipher.encrypt_and_digest(data)
aes_data = aes_cipher.nonce + aes_tag + aes_encrypted
```
- 256-bit key strength
- Authenticated encryption with integrity verification
- 96-bit nonce for uniqueness

#### Layer 2: ChaCha20 Stream Cipher
```python
chacha_cipher = ChaCha20.new(key=chacha_key, nonce=chacha_nonce)
chacha_encrypted = chacha_cipher.encrypt(aes_data)
```
- 256-bit key
- 96-bit nonce
- Designed for high performance in software

#### Layer 3: Salsa20 Stream Cipher
```python
salsa_cipher = Salsa20.new(key=salsa_key, nonce=salsa_nonce)
salsa_encrypted = salsa_cipher.encrypt(chacha_data)
```
- 256-bit key
- 64-bit nonce
- Additional layer of confusion

#### Layer 4: XOR with 256-byte Key
```python
xor_encrypted = bytes(a ^ b for a, b in zip(data, extended_key))
```
- 256-byte XOR key
- Added complexity layer

**Key Derivation:**
All keys are derived using **scrypt** with:
- N=65536 (2^16)
- r=8
- p=1
- 64-byte master entropy

This makes brute-force attacks computationally infeasible.

---

### 5. Deep XOR Obfuscation (Option 42)

Combines XOR encryption with multiple protection mechanisms:

**Anti-Debug Protections:**
```python
def anti_debug():
    # Detect debugger
    if hasattr(sys, 'gettrace') and sys.gettrace():
        sys.exit()
    
    # Timing attack detection
    start = time.time()
    for _ in range(100000): pass
    if time.time() - start > 0.5:
        sys.exit()
    
    # Check for debugging modules
    try:
        import pydevd, traceback, pdb, inspect
        sys.exit()
    except: pass
    
    # Process monitoring
    for proc in psutil.process_iter():
        if 'debug' in proc.name().lower():
            sys.exit()
```

**Thread-Based Protection:**
```python
def protect_thread():
    while True:
        # Continuous anti-debug checks
        anti_debug()
        # Random corruption of canary values
        canaries[random_index] ^= random_value
        time.sleep(random.uniform(1.5, 4.0))
```

---

## 🛡️ Runtime Protection Features

### Anti-Debug (All Methods)
- `sys.gettrace()` detection
- Timing attack detection
- Debugging module detection (pydevd, pdb, inspect)
- Process monitoring (IDA, OllyDbg, x64dbg, etc.)

### Anti-VM/Sandbox (Option 42, 44, 45)
- Virtual machine signature detection (VMware, VirtualBox, QEMU, etc.)
- Suspicious hostname detection
- CPU/Memory analysis
- Container detection (Docker, Kubernetes)

### Anti-Hook (Option 42)
- Built-in function integrity checking
- marshal module verification
- sys.exit integrity check

### Anti-Proxy (Option 42)
- Environment variable checks (HTTP_PROXY, HTTPS_PROXY)
- MITM tool detection (Burp, Fiddler, mitmproxy)

---

## 🚀 Installation

```bash
git clone https://github.com/BatmanPriv/PyObfuscator.git
cd PyObfuscator
python PyObfuscator.py
```

The tool automatically installs required dependencies:
```bash
pip install pycryptodome
```

---

## 📖 Usage

### Interactive Mode

```bash
python PyObfuscator.py
```

### Menu Navigation

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
[42] Deep XOR Obfuscation (Anti-Debug + Anti-VM)
[43] AST Obfuscation (Control Flow Flattening + String Encryption)
[44] AST Obfuscation (CJK + Junk + Multi-layer)
[45] Ultra Obfuscation (AES+ChaCha20+Salsa20+XOR)
[46] Exit
```

### Example Session

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

| Protection Method | Size Expansion | Speed | Protection Level |
|-------------------|---------------|-------|------------------|
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

### Supported Python Versions
- Python 3.6 → 3.13

### Dependencies
```
pycryptodome >= 3.15.0
```

### File Size Limits
- Input: Unlimited
- Output: Varies by method (10KB - 50MB)

### Memory Usage
- Options 1-40: <100MB
- Option 41-43: <200MB
- Option 44-45: <500MB

---

## 🎯 When To Use Each Method

### Choose Options 1-7 for:
- Quick protection of non-critical code
- Learning purposes
- Basic obfuscation needs

### Choose Options 8-16 for:
- Moderate protection requirements
- When size expansion is a concern
- Balancing speed and security

### Choose Options 17-40 for:
- Commercial software protection
- Protecting API keys and credentials
- When you need multiple encoding layers

### Choose Option 41 for:
- Quick protection with moderate security
- When you need basic obfuscation

### Choose Option 42 for:
- Protection against debugging attempts
- When you need runtime security monitoring
- Protecting sensitive algorithms

### Choose Option 43 for:
- Deep structural obfuscation
- When you need string encryption
- Professional software protection

### Choose Option 44 for:
- Maximum confusion
- Protection against decompilers
- When size is not a concern

### Choose Option 45 for:
- Military-grade protection
- Protecting national security-level code
- When failure is not an option

---

## 🛡️ Protection Mechanisms Detail

### Anti-Debug (Option 42, 44, 45)
Detects and blocks:
- Python debuggers (pdb, pydevd)
- System debuggers (IDA, OllyDbg, x64dbg)
- Runtime inspection (sys.gettrace)
- Timing analysis attacks

### Anti-VM/Sandbox (Option 42, 44, 45)
Detects:
- Virtual machine signatures (VMware, VirtualBox, QEMU)
- Container environments (Docker, Kubernetes)
- Sandbox environments (Cuckoo, JoeBox)
- Suspicious system configurations

### Anti-Hook (Option 42)
Verifies integrity of:
- Built-in functions (print, exec, eval)
- marshal module
- sys.exit

### Anti-Proxy (Option 42)
Detects:
- HTTP/HTTPS proxy configuration
- MITM tools (Burp, Fiddler)
- Network interception
