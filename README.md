# Padding Oracle Attack  CBC Mode Showcase

A visual, interactive demonstration of the **Padding Oracle Attack** on **AES-128 in CBC mode**, built with Python and Tkinter. This project implements AES-128 encryption/decryption from scratch (no external crypto libraries), simulates a vulnerable server that leaks padding validity, and walks through a live brute-force decryption attack, byte by byte.

---

## Table of Contents

- [What is a Padding Oracle Attack?](#what-is-a-padding-oracle-attack)
- [How This Project Works](#how-this-project-works)
- [Required Software](#required-software)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Usage Guide](#usage-guide)
- [Project Structure](#project-structure)
- [Technical Details](#technical-details)
- [Security](#security)
- [License](#license)

---

## What is a Padding Oracle Attack?

A **Padding Oracle Attack** is a cryptographic side-channel attack that allows an attacker to decrypt ciphertext **without knowing the encryption key**, by repeatedly querying a vulnerable server that reveals whether the decrypted padding is valid or not.

### The Core Idea

In CBC (Cipher Block Chaining) mode, decryption of each block involves:
```
Plaintext Block = AES_Decrypt(Ciphertext Block) XOR Previous Ciphertext Block (or IV)
```

After decryption, PKCS#7 padding is checked. If the padding is **invalid**, the server returns an error -- this error is the "oracle." An attacker can:

1. Craft a modified IV (or previous ciphertext block)
2. Submit it to the server
3. Observe whether padding is valid or not
4. Use this yes/no signal to recover the intermediate decryption value byte-by-byte
5. XOR the intermediate value with the real IV to recover the original plaintext

This attack requires **up to 256 x block_size** queries per block (worst case), making it practical against systems that leak padding errors.

---

## How This Project Works

The app has two sections, accessible via a tabbed GUI:

**Server/Client Communication** -- Enter a plaintext string and an IV (hex). The server encrypts it using AES-128 CBC (implemented from scratch). You simulate a client sending the token back -- either with a tampered IV (bad padding = 500 error) or the original token (good padding = 200 OK). This illustrates how a real server leaks padding validity through its HTTP response codes.

**Padding Oracle Attack** -- The attacker uses the padding oracle from the first section to recover the plaintext. The GUI visualizes in real time: the intermediate decryption output (`Dk`) per byte, the brute-forced IV' block being tried, the recovered plaintext bytes as they are found, and the total oracle queries made.

---

## Required Software

> [!NOTE]  
> No external libraries are used — everything (including AES) is implemented from scratch for educational purposes.

Python 3.7 or higher is the only runtime dependency. All cryptographic logic and the GUI are implemented using Python's standard library.

| Dependency | Version | Notes |
|---|---|---|
| **Python** | 3.7+ | Core runtime |
| **tkinter** | Bundled with Python | GUI framework |
| **os** | Built-in | Used for `os.urandom()` (key/IV generation) |

No third-party packages are required. No `pip install` needed.

---

## Installation

**1. Verify Python is installed**
```bash
python3 --version
```

Expected: `Python 3.x.x` (3.8 or higher). If Python is not installed, see the [official downloads page](https://www.python.org/downloads/).

**2. Verify tkinter is available**

> [!WARNING]  
> If `tkinter` is missing, the GUI will not launch.

```bash
python3 -c "import tkinter; print('tkinter OK')"
```

If tkinter is missing, install it for your platform:

  - Ubuntu/Debian: `sudo apt install python3-tk`
  - Fedora: `sudo dnf install python3-tkinter`
  - macOS (Homebrew): `brew install python-tk`
  - Windows: Reinstall Python from [python.org](https://www.python.org/downloads/) with "tcl/tk and IDLE" checked

**3. Clone the repository**

```bash
git clone https://github.com/ppmpreetham/crypto_project.git
cd crypto_project
```

**4. Setup Virtual Environment & Install Dependencies**

We recommend using the provided quick-start scripts to automatically create a virtual environment and install the requirements.

**Using Provided Scripts:**

  - **Windows:** Run `.\run.ps1` in PowerShell.
  - **Linux/macOS:** Run `chmod +x run.sh && ./run.sh` in your terminal.

---

## Usage Guide

> [!NOTE]  
> This project is interactive. Follow the steps in order to fully understand how the padding oracle attack works.

### Server/Client Communication

> [!TIP]
> Try different plaintext values and IVs to observe how small changes affect ciphertext and padding behavior.

1. Open the app and go to the **"Server/Client Comm"** tab.

2. In the **"Server: Prepare Token"** section:
   - **Plaintext**: Enter any text to encrypt (e.g. `SECRET`, `admin`, `hello world`).
   - **IV (Hex)**: A random 16-byte IV is pre-filled. Leave it or replace with your own 32-character hex string.

3. Click **"Encrypt & Create Token"**. The log panel shows the padded plaintext (hex), the full packet (`IV || Ciphertext`), and a confirmation.

4. In the **"Client: Send Token to Server"** section:
   - **"Send Token (Bad Padding)"** -- simulates an attacker flipping bits in the IV, causing a padding error. The log shows a `500 Internal Error`.
   - **"Send Token (Good Padding)"** -- simulates sending the original token. The log shows `200 OK`.

   This models the real-world scenario where a server's differing error responses for valid vs. invalid padding expose an oracle.

### Padding Oracle Attack

> [!IMPORTANT]  
> You must complete the encryption step in the **Server/Client Communication** tab before starting the attack.

> [!NOTE]  
> The attack works one byte at a time and may take several seconds depending on system performance.

1. Switch to the **"Padding Oracle Attack"** tab. The top section displays the original plaintext, IV, and ciphertext.

2. Click **"Start Padding Oracle Attack"**.

3. Watch the live visualization:
   - **Dk Output (Intermed.)**: Raw block cipher output, recovered byte by byte (blue). `??` placeholders fill in as bytes are found.
   - **Bruteforce Block IV'**: The crafted IV tested against the oracle each round (red).
   - **Clear Text Bytes (Pt)**: Recovered plaintext bytes revealed as the attack progresses (green).
   - **Status bar**: Current block, byte index, current guess (0x00-0xFF), and total oracle requests.

4. When complete, the status bar displays:
```
   Attack Complete! Total Requests: XXXX
   Decrypted Text: 'your original message'
```

---

## Project Structure
```
crypto_project/
├── padding_oracle.py   # Crypto engine + GUI
├── SECURITY.md         # Vulnerability reporting policy
└── LICENSE             # MIT License
```

All logic lives in a single file:

| Component | Description |
|---|---|
| `SBOX` / `INV_SBOX` | AES S-box and inverse S-box lookup tables |
| `RCON` | Round constants for AES key expansion |
| `gmul()` | Galois Field multiplication (GF(2^8)) |
| `key_expansion()` | AES-128 key schedule (11 round keys) |
| `aes_encrypt_block()` | Single AES-128 block encryption (10 rounds) |
| `aes_decrypt_block()` | Single AES-128 block decryption (10 rounds) |
| `pkcs7_pad()` / `pkcs7_unpad()` | PKCS#7 padding and validation |
| `encrypt_cbc()` / `decrypt_cbc()` | Full CBC mode encrypt/decrypt |
| `padding_oracle()` | The oracle: returns `True` if padding is valid, `False` otherwise |
| `PaddingOracleApp` | Tkinter GUI with two-section interactive showcase |

---

## Technical Details

### AES-128 Implementation

No `cryptography`, `pycryptodome`, or external library is used. The implementation covers all AES internals: SubBytes, ShiftRows, MixColumns, AddRoundKey, using the real AES S-box and GF(2^8) arithmetic for MixColumns. The key is generated using `os.urandom(16)` at startup.

### CBC Mode

Each plaintext block is XOR'd with the previous ciphertext block (or IV for the first block) before encryption. Decryption reverses this: each block is decrypted then XOR'd with the prior ciphertext block. This chaining means a 1-bit change to the IV or any ciphertext block affects decryption.

### PKCS#7 Padding

> [!CAUTION]
> Incorrect padding handling is the root cause of padding oracle vulnerabilities.

Padding is added so plaintext length is a multiple of 16 bytes. If the last block needs `n` bytes of padding, it is filled with `n` bytes of value `n`:
```
"HELLO" -> "HELLO\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b"
```

If padding is incorrect after decryption, a `ValueError` is raised -- this is the error the oracle exposes.

### The Attack Algorithm (Per Block)

> [!NOTE]  
> Each byte may require up to 256 attempts, making this a computationally intensive process.

For each byte position `i` from 15 down to 0:

1. Set padding target = `16 - i`
2. For already-known bytes (positions > i), compute IV' bytes so they decrypt to the target padding value
3. Brute-force position `i` (0x00 to 0xFF, up to 256 guesses) until padding is valid
4. When valid: `Dk[i] = guess XOR pad_target`, then `Pt[i] = Dk[i] XOR original_IV[i]`
5. Repeat for all 16 bytes

Worst case: **256 x 16 = 4,096** oracle queries per 16-byte block.

---

## Security

> [!WARNING]  
> This project intentionally demonstrates a real cryptographic vulnerability. Do NOT use this code in production.

> [!IMPORTANT]  
> The implementation is designed for learning purposes and lacks protections required for secure systems.

See [SECURITY.md](SECURITY.md) for the vulnerability reporting policy.

The Padding Oracle Attack is a real, well-documented vulnerability that has affected production systems including ASP.NET ([CVE-2010-3332](https://www.cve.org/CVERecord?id=CVE-2010-3332)) and many SSL/TLS implementations. Modern secure systems mitigate this by:

- Using **authenticated encryption** (AES-GCM, ChaCha20-Poly1305) instead of CBC + PKCS#7
- Applying a **MAC-then-encrypt** or **encrypt-then-MAC** scheme correctly
- Returning **uniform error messages** regardless of whether the failure was in decryption or padding (though this alone is insufficient)

---

## License

> [!NOTE]  
> You are free to use, modify, and distribute this project under the MIT License.
This project is licensed under the **MIT License** -- see the [LICENSE](LICENSE) file for details.

Copyright (c) 2026 Preetham Pemmasani
