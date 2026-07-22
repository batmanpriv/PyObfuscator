# PyObfuscator

**Advanced Python Code Obfuscation Engine**  
*A comprehensive toolkit for protecting Python source code through multi-layer encryption and AST-level transformations*

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0-brightgreen.svg)]()

---

## 📌 Overview

PyObfuscator is a professional-grade Python obfuscation tool offering **45 distinct protection methods**, ranging from simple encoding to advanced AST manipulation and multi-layer cryptographic protection. Each technique is designed to make reverse engineering, decompilation, and code analysis significantly more difficult.

> **Developer:** [@BatmanPriv](https://t.me/BatmanPriv)

---

## 📸 Interface Preview

<img src="https://github.com/user-attachments/assets/036d7eb8-66d0-4d54-af9a-ce7f57ccf891">

---

## ⚡ Obfuscation Methods

### Encoding-Based Methods (Options 1–40)

| Method | Description | Protection Level |
|--------|-------------|------------------|
| 1–7 | **Single-layer** (Marshal, Zlib, GZIP, LZMA, Base16/32/64) | Low |
| 8–16 | **Two-layer** (Compression + Encoding combinations) | Medium |
| 17–31 | **Marshal + Compression/Encoding** | Medium-High |
| 32–40 | **Multi-layer** (3-5 layers combining Marshal, Zlib, LZMA, GZIP, Base64) | High |

### Advanced Obfuscation Methods (Options 41–45)

| Option | Method | Description |
|--------|--------|-------------|
| **41** | Simple Obfuscation | 5-layer nested compression + marshaling with dynamic decoding |
| **42** | Deep XOR Obfuscation | XOR encryption with recursive wrapper layers and anti-tamper checks |
| **43** | AST Obfuscation | Control flow flattening, variable renaming, string encryption (AES-256-CBC) |
| **44** | CJK Obfuscation | AST transformation with CJK variable names + dead code injection + 10-layer protection pipeline |
| **45** | Ultra Obfuscation | Quadruple-layer cryptographic protection (AES-256-GCM + ChaCha20 + Salsa20 + XOR) |

---

## 🧠 Technical Deep Dive

### 1. AST-Level Transformation (Option 43)

Operates directly on Python's Abstract Syntax Tree before compilation:

**Control Flow Flattening**  
Converts structured code with nested conditions and loops into a flat state-machine:
```python
# Original
if x > 0:
    do_something()
else:
    do_other()

# Transformed
state = 0
while state < 2:
    if state == 0:
        if x > 0:
            do_something()
        state = 1
    elif state == 1:
        do_other()
        state = 2
```
This eliminates predictable control flow, making manual analysis and automated deobfuscation significantly harder.

**Variable Renaming**  
All user-defined variable names are replaced with deterministic yet meaningless identifiers (`v_3a8f2b1c`), breaking semantic understanding.

**String Encryption**  
All string literals are encrypted using AES-256-CBC with unique initialization vectors per string. Runtime decryption occurs via injected decryption functions.

### 2. CJK Obfuscation (Option 44)

This method is designed to defeat decompilers and confuse human readers through extensive code injection:

**CJK Variable Names**  
Variables are named using Korean (Hangul), Chinese (Hanzi), and Japanese (Kana) characters:
```python
홁 = [2847 for _ in range(45)]
鰿 = {(lambda 鍘: 鍘 ^ 127)(i) for i in range(30)}
桽 = [(lambda 鼜, 鰪: 鼜 * 鰪)(i, j) for i in range(67)]
```
These characters are valid Python identifiers but are visually confusing and cause syntax highlighters and decompilers to malfunction.

**Dead Code Injection**  
Hundreds of lines of meaningless operations are injected: list comprehensions, nested lambdas, dictionary comprehensions, and long CJK comment blocks. This increases code size by 15-30x and creates massive amounts of junk data for analysis tools to process.

**Multi-Layer Protection Pipeline**  
```
Original Source Code
    ↓
AST Transformation (Flatten + Rename + String Encryption)
    ↓
Marshal Serialization
    ↓
Zlib Compression (Level 9) — First pass
    ↓
Zlib Compression (Level 9) — Second pass
    ↓
BZ2 Compression
    ↓
LZMA Compression
    ↓
Base85 Encoding
    ↓
XOR-32 (32-byte random key)
    ↓
Shuffle Permutation (random index reordering)
    ↓
RC4 Encryption (16-byte random key)
    ↓
LCG-XOR (Linear Congruential Generator)
    ↓
Base64 Encoding
    ↓
Final Protected Code
```

**Key Features:**
- Each layer uses different algorithms, preventing single-point decryption
- Shuffle layer breaks pattern recognition in compressed data
- LCG-XOR creates pseudo-random output resistant to statistical analysis
- Compression before encryption removes data redundancy

### 3. Ultra Obfuscation (Option 45)

**Quadruple-Layer Encryption Architecture:**

| Layer | Algorithm | Key Size | Nonce/IV | Purpose |
|-------|-----------|----------|----------|---------|
| 1 | AES-256-GCM | 256-bit | 96-bit | Authenticated encryption with integrity |
| 2 | ChaCha20 | 256-bit | 96-bit | High-performance stream cipher |
| 3 | Salsa20 | 256-bit | 64-bit | Additional confusion layer |
| 4 | XOR | 256-byte | N/A | Final transformation layer |

**Key Derivation:**  
All encryption keys are derived from a 64-byte master entropy using **scrypt**:
```python
scrypt(master_entropy, salt, N=65536, r=8, p=1)
```
With these parameters, a single key derivation requires ~100ms of CPU time, making brute-force attacks computationally infeasible.

**Runtime Protection:**  
The generated loader includes:
- Random shuffling of decoy functions
- Randomized execution patterns
- Secret token generation for anti-debugging
- Automatic pycryptodome installation if missing

### 4. Deep XOR Obfuscation (Option 42)

Implements XOR-based encryption with:
- 16-byte or custom XOR key
- Configurable recursive wrapper layers (default: 4)
- Zlib compression before encryption
- Base64 encoding of encrypted data
- Runtime decryption with anti-debugging checks
- Background thread execution for detection evasion

### 5. Encoding Chain System (Options 1–40)

The CodecEngine provides a flexible encoding pipeline supporting combinations of:
- **Serialization:** Marshal (`marshal.dumps`/`loads`)
- **Compression:** Zlib, GZIP, LZMA
- **Encoding:** Base16, Base32, Base64

Each combination uses reverse-order decoding, and all encoded data is byte-reversed for additional obfuscation.

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/batmanpriv/PyObfuscator.git
cd PyObfuscator

# Run the tool (auto-installs pycryptodome if missing)
python PyObfuscator.py
```

**Requirements:**
- Python 3.6 or higher
- pycryptodome (auto-installed if missing)
- Standard library modules (all included in Python distribution)

---

## 📖 Usage Guide

### Basic Usage

```bash
python PyObfuscator.py
```

Follow the interactive menu:
1. Select an obfuscation method (1–45)
2. Enter the path to your Python file
3. For methods requiring additional input:
   - **Option 42:** Custom key (optional) and number of layers
   - All other methods: Encoding loop count (number of times to re-encode)

### Examples

**Example 1: Basic Protection**
```bash
$ python PyObfuscator.py
[+] Option: 10
[+] File Name: script.py
[+] Encode Count: 5
[+] Obfuscation complete: script_obfuscated.py
[+] Size: 12.3 KB
```

**Example 2: Maximum Protection**
```bash
$ python PyObfuscator.py
[+] Option: 45
[+] File Name: sensitive.py
[+] Encode Count: 3
[+] Obfuscation complete: sensitive_ultra.py
[+] Size: 184.7 KB
```

### Method Selection Guide

| Use Case | Recommended Method(s) |
|----------|----------------------|
| Quick basic protection | 1–7 |
| Moderate protection with minimal size increase | 8–16 |
| Commercial software protection | 17–40, 43 |
| Protection against decompilers | 44 |
| Maximum security | 45 |
| API key / credential protection | 42–45 |

---

## 📊 Performance Characteristics

| Method Group | Size Expansion | Processing Time | Memory Usage | Security Level |
|--------------|---------------|-----------------|--------------|----------------|
| Options 1–7 | 1.5–2x | <1s | <50MB | Basic |
| Options 8–16 | 2–3x | <2s | <100MB | Medium |
| Options 17–31 | 3–4x | 2–4s | <150MB | High |
| Options 32–40 | 4–5x | 3–5s | <200MB | Very High |
| Option 41 | 2–3x | <2s | <100MB | Medium |
| Option 42 | 5–8x | 3–7s | <200MB | High |
| Option 43 | 8–12x | 4–8s | <250MB | Very High |
| Option 44 | 15–30x | 5–10s | <500MB | Extreme |
| Option 45 | 10–20x | 3–6s | <300MB | Military-Grade |

---

## 🔧 Technical Specifications

**Supported Python Versions:** 3.6 – 3.13

**Dependencies:**
- `pycryptodome` >= 3.15.0 (auto-installed)

**Input File Limits:**
- Encoding methods: Unlimited
- AST methods: Recommended < 10MB
- CJK method: Recommended < 5MB

**Output File Characteristics:**
- Method 44: 200–500 lines of garbage code injected
- Method 45: AES-256-GCM + ChaCha20 + Salsa20 + XOR protected
- All outputs: Compiled with `py_compile` for .pyc generation

**Anti-Analysis Features:**
- All AST transformations preserve original functionality
- No external API calls (except pycryptodome installation)
- Self-contained obfuscated output

---

## 🎯 Comparison Table

| Feature | Options 1–40 | Option 41 | Option 42 | Option 43 | Option 44 | Option 45 |
|---------|-------------|-----------|-----------|-----------|-----------|-----------|
| Encoding/Compression | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| XOR Encryption | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ |
| Control Flow Flattening | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| Variable Renaming | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| String Encryption | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| CJK Variables | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| Dead Code Injection | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| Multi-Cipher Encryption | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Decompiler Resistance | Low | Medium | High | Very High | Extreme | Extreme |

---

## 🛠️ Architecture

```
PyObfuscator.py
├── EnvironmentValidator     # Python version & import validation
├── CodecEngine             # Encoding/decoding operations
├── XOREngine              # XOR encryption utilities
├── ASTObfuscator          # AST-level transformations
│   ├── VariableCollector
│   ├── VariableRenamer
│   ├── ControlFlowFlattener
│   └── StringEncryptor
├── CJKObfuscator          # CJK-based obfuscation
├── UltraObfuscator        # Multi-layer encryption
├── ObfuscatorEngine       # Core obfuscation logic
├── Interface              # CLI menu & display
└── PyObfuscator           # Main application entry
```

---

## ⚠️ Important Notes

**Performance Considerations:**
- Methods 44–45 significantly increase file size (15-30x)
- Processing time increases with code complexity
- Memory usage peaks during AST transformations

**Compatibility:**
- Output files require Python 3.6+
- Some obfuscated code may trigger antivirus false positives
- Use of `exec()` in output is required for dynamic decoding

**Security:**
- No method provides absolute protection
- Obfuscation makes analysis harder, not impossible
- Always test obfuscated code before deployment

---

## 📝 License

This project is licensed under the MIT License.

---

**Developed by [@BatmanPriv](https://t.me/BatmanPriv)**  
*For educational and legitimate protection purposes only.*
