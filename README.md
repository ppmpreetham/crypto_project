# 🔐 Padding Oracle Attack — CBC Mode Showcase

A visual, interactive demonstration of the **Padding Oracle Attack** on **AES-128 in CBC mode**, built with Python and Tkinter. This project implements AES-128 encryption/decryption from scratch (no external crypto libraries), simulates a vulnerable server that leaks padding validity, and walks through a live brute-force decryption attack — byte by byte.

---

## 📚 Table of Contents

- [What is a Padding Oracle Attack?](#what-is-a-padding-oracle-attack)
- [How This Project Works](#how-this-project-works)
- [Required Software](#required-software)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Step-by-Step Usage Guide](#step-by-step-usage-guide)
- [Project Structure](#project-structure)
- [Technical Details](#technical-details)
- [Security Note](#security-note)
- [License](#license)

---

## What is a Padding Oracle Attack?

A **Padding Oracle Attack** is a cryptographic side-channel attack that allows an attacker to decrypt ciphertext **without knowing the encryption key**, by repeatedly querying a vulnerable server that reveals whether the decrypted padding is valid or not.

### The Core Idea

In CBC (Cipher Block Chaining) mode, decryption of each block involves:

```
Plaintext Block = AES_Decrypt(Ciphertext Block) XOR Previous Ciphertext Block (or IV)
```

After decryption, PKCS#7 padding is checked. If the padding is **invalid**, the server returns an error — this error is the "oracle." An attacker can:

1. Craft a modified IV (or previous ciphertext block)
2. Submit it to the server
3. Observe whether padding is valid or not
4. Use this yes/no signal to recover the intermediate decryption value byte-by-byte
5. XOR the intermediate value with the real IV to recover the original plaintext

This attack requires **up to 256 × block_size** queries per block (worst case), making it practical against systems that leak padding errors.

---

## How This Project Works

The app is split into **two phases**, both accessible via a tabbed GUI:

### Phase 1: Server/Client Communication
- You enter a plaintext string and an IV (hex)
- The server encrypts it using AES-128 CBC (implemented from scratch)
- You simulate a client sending the token back — either with a **tampered IV** (bad padding → 500 error) or the **original token** (good padding → 200 OK)
- This illustrates how a real server leaks padding validity through its HTTP response codes

### Phase 2: Padding Oracle Attack
- The attacker uses the padding oracle from Phase 1 to recover the plaintext
- The GUI visualizes, in real time:
  - The **intermediate decryption output** (`Dk`) per byte
  - The **brute-forced IV'** block being tried
  - The **recovered plaintext bytes** as they are found
  - Total oracle queries made

---

## Required Software

### Python 3.7 or higher

Python is the only runtime dependency. All cryptographic logic and the GUI are implemented using Python's standard library.

| Dependency | Version | Notes |
|---|---|---|
| **Python** | 3.7+ | Core runtime |
| **tkinter** | Bundled with Python | GUI framework |
| **os** | Built-in | Used for `os.urandom()` (key/IV generation) |

> **No third-party packages are required.** No `pip install` needed.

---

## Installation

### Step 1 — Verify Python is installed

```bash
python --version
# or
python3 --version
```

Expected output: `Python 3.x.x` (3.7 or higher)

If Python is not installed:
- **Windows/macOS**: Download from [python.org](https://www.python.org/downloads/)
- **Ubuntu/Debian**: `sudo apt install python3`
- **Fedora/RHEL**: `sudo dnf install python3`
- **Arch Linux**: `sudo pacman -S python`

---

### Step 2 — Verify tkinter is available

```bash
python -c "import tkinter; print('tkinter OK')"
# or
python3 -c "import tkinter; print('tkinter OK')"
```

If you see `tkinter OK`, you're good to go.

**If tkinter is missing:**

- **Ubuntu/Debian**:
  ```bash
  sudo apt install python3-tk
  ```
- **Fedora**:
  ```bash
  sudo dnf install python3-tkinter
  ```
- **macOS (Homebrew Python)**:
  ```bash
  brew install python-tk
  ```
- **Windows**: Reinstall Python from [python.org](https://www.python.org/downloads/) and ensure "tcl/tk and IDLE" is checked during setup.

---

### Step 3 — Clone the repository

```bash
git clone https://github.com/ppmpreetham/crypto_project.git
cd crypto_project
```

Or download the ZIP directly from GitHub → **Code → Download ZIP**, then extract it.

---

## Running the Project

```bash
python padding_oracle.py
# or
python3 padding_oracle.py
```

This launches the GUI window titled **"Padding Oracle Attack Showcase"**.

---

## Step-by-Step Usage Guide

### Phase 1 — Simulating Server/Client Communication

1. Open the app. You'll land on the **"Phase 1: Server/Client Comm"** tab.

2. In the **"Server: Prepare Token"** section:
   - **Plaintext**: Enter any text you want to encrypt (e.g., `SECRET`, `admin`, `hello world`). This is the message the server wants to protect.
   - **IV (Hex)**: A random 16-byte IV is pre-filled. You can leave it as-is or replace it with your own 32-character hex string.

3. Click **"Encrypt & Create Token"**.
   - The log panel will show the padded plaintext (hex), the full packet (`IV || Ciphertext`), and confirmation that the token is ready.

4. In the **"Client: Send Token to Server"** section:
   - Click **"Send Token (Bad Padding)"** — simulates an attacker flipping bits in the IV, causing a padding error. The log shows a `500 Internal Error`.
   - Click **"Send Token (Good Padding)"** — simulates sending the original token. The log shows `200 OK`.

   > This models the real-world scenario where a server's different error responses for valid vs. invalid padding expose an oracle.

---

### Phase 2 — Running the Padding Oracle Attack

1. Switch to the **"Phase 2: Padding Oracle Attack"** tab.

   > ⚠️ You **must** complete Phase 1 (encrypt a token) before running the attack.

2. The top section displays the:
   - **Input Text** — the original plaintext
   - **Original IV** — the IV used during encryption
   - **Cipher Text** — the ciphertext the attacker is trying to decrypt

3. Click **"Start Padding Oracle Attack"**.

4. Watch the live visualization:
   - **Dk Output (Intermed.)**: The raw block cipher output, recovered byte by byte (shown in blue). `??` placeholders fill in from left as bytes are found.
   - **Bruteforce Block IV'**: The crafted IV being tested against the oracle each round (shown in red).
   - **Clear Text Bytes (Pt)**: The recovered plaintext bytes, revealed as the attack progresses (shown in green).
   - **Status bar**: Shows current block, byte index, current guess (0x00–0xFF), and total oracle requests made.

5. When the attack completes, the status bar displays:
   ```
   Attack Complete! Total Requests: XXXX
   Decrypted Text: 'your original message'
   ```

---

## Project Structure

```
crypto_project/
├── padding_oracle.py   # The entire project — crypto engine + GUI
└── LICENSE             # MIT License
```

All logic lives in a single file:

| Component | Description |
|---|---|
| `SBOX` / `INV_SBOX` | AES S-box and inverse S-box lookup tables |
| `RCON` | Round constants for AES key expansion |
| `gmul()` | Galois Field multiplication (GF(2⁸)) |
| `key_expansion()` | AES-128 key schedule (11 round keys) |
| `aes_encrypt_block()` | Single AES-128 block encryption (10 rounds) |
| `aes_decrypt_block()` | Single AES-128 block decryption (10 rounds) |
| `pkcs7_pad()` / `pkcs7_unpad()` | PKCS#7 padding and validation |
| `encrypt_cbc()` / `decrypt_cbc()` | Full CBC mode encrypt/decrypt |
| `padding_oracle()` | The oracle: returns `True` if padding is valid, `False` otherwise |
| `PaddingOracleApp` | Tkinter GUI with two-phase interactive showcase |

---

## Technical Details

### AES-128 Implementation

- **Custom from scratch**: no `cryptography`, `pycryptodome`, or any external library is used
- Implements all AES internals: SubBytes, ShiftRows, MixColumns, AddRoundKey
- Uses the real AES S-box and GF(2⁸) arithmetic for MixColumns
- Key is generated using `os.urandom(16)` at startup (16 random bytes = 128-bit key)

### CBC Mode

- Each plaintext block is XOR'd with the previous ciphertext block (or IV for the first block) before encryption
- Decryption reverses this: each block is decrypted then XOR'd with the prior ciphertext block
- This chaining means **a 1-bit change to the IV or any ciphertext block affects decryption**

### PKCS#7 Padding

Padding is added so plaintext length is a multiple of 16 bytes. If the last block needs `n` bytes of padding, it is filled with `n` bytes of value `n`:

```
"HELLO" → "HELLO\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b"
```

If padding is incorrect after decryption, a `ValueError` is raised — this is the error the oracle exposes.

### The Attack Algorithm (Per Block)

For each byte position `i` from 15 down to 0:

1. Set padding target = `16 - i`
2. For already-known bytes (positions > i), compute IV' bytes so they decrypt to the target padding value
3. Brute-force position `i` (0x00 → 0xFF, up to 256 guesses) until padding is valid
4. When valid: `Dk[i] = guess XOR pad_target`, then `Pt[i] = Dk[i] XOR original_IV[i]`
5. Repeat for all 16 bytes

Worst case: **256 × 16 = 4,096** oracle queries per 16-byte block.

---

## Security Note

> ⚠️ **This project is strictly educational.**

The Padding Oracle Attack is a real, well-documented vulnerability that has affected production systems including ASP.NET (CVE-2010-3332) and many SSL/TLS implementations. Modern secure systems mitigate this by:

- Using **authenticated encryption** (AES-GCM, ChaCha20-Poly1305) instead of CBC + PKCS#7
- Applying a **MAC-then-encrypt** or **encrypt-then-MAC** scheme correctly
- Returning **uniform error messages** regardless of whether the failure was in decryption or padding (though this alone is insufficient)

Do not use this code in any production or security-sensitive context.

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

Copyright © 2026 Preetham Pemmasani
