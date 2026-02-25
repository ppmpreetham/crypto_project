import tkinter as tk
from tkinter import ttk, messagebox
import os

BLOCK_SIZE = 16

SBOX = [
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
]

INV_SBOX = [
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D
]

RCON = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]

AES_KEY = os.urandom(16)

def gmul(a, b):
    p = 0
    for _ in range(8):
        if b & 1: p ^= a
        hi_bit_set = a & 0x80
        a = (a << 1) & 0xFF
        if hi_bit_set: a ^= 0x1B  
        b >>= 1
    return p

def key_expansion(key):
    key_symbols = [b for b in key]
    for i in range(16, 176, 4):
        temp = key_symbols[i-4:i]
        if i % 16 == 0:
            temp = [SBOX[temp[1]], SBOX[temp[2]], SBOX[temp[3]], SBOX[temp[0]]]
            temp[0] ^= RCON[i // 16]
        key_symbols.extend([key_symbols[i-16+j] ^ temp[j] for j in range(4)])
    return [key_symbols[i:i+16] for i in range(0, 176, 16)]

AES_ROUND_KEYS = key_expansion(AES_KEY)

def aes_encrypt_block(block: bytes) -> bytes:
    state = list(block)
    state = [s ^ k for s, k in zip(state, AES_ROUND_KEYS[0])]
    for round in range(1, 11):
        state = [SBOX[b] for b in state]
        state = [
            state[0], state[5], state[10], state[15],
            state[4], state[9], state[14], state[3],
            state[8], state[13], state[2], state[7],
            state[12], state[1], state[6], state[11]
        ]
        if round < 10:
            new_state = [0] * 16
            for c in range(4):
                col = state[c*4:(c+1)*4]
                new_state[c*4+0] = gmul(col[0], 2) ^ gmul(col[1], 3) ^ col[2] ^ col[3]
                new_state[c*4+1] = col[0] ^ gmul(col[1], 2) ^ gmul(col[2], 3) ^ col[3]
                new_state[c*4+2] = col[0] ^ col[1] ^ gmul(col[2], 2) ^ gmul(col[3], 3)
                new_state[c*4+3] = gmul(col[0], 3) ^ col[1] ^ col[2] ^ gmul(col[3], 2)
            state = new_state
        state = [s ^ k for s, k in zip(state, AES_ROUND_KEYS[round])]
    return bytes(state)

def aes_decrypt_block(block: bytes) -> bytes:
    state = list(block)
    state = [s ^ k for s, k in zip(state, AES_ROUND_KEYS[10])]
    for round in range(9, -1, -1):
        state = [
            state[0], state[13], state[10], state[7],
            state[4], state[1], state[14], state[11],
            state[8], state[5], state[2], state[15],
            state[12], state[9], state[6], state[3]
        ]
        state = [INV_SBOX[b] for b in state]
        state = [s ^ k for s, k in zip(state, AES_ROUND_KEYS[round])]
        if round > 0:
            new_state = [0] * 16
            for c in range(4):
                col = state[c*4:(c+1)*4]
                new_state[c*4+0] = gmul(col[0], 14) ^ gmul(col[1], 11) ^ gmul(col[2], 13) ^ gmul(col[3], 9)
                new_state[c*4+1] = gmul(col[0], 9) ^ gmul(col[1], 14) ^ gmul(col[2], 11) ^ gmul(col[3], 13)
                new_state[c*4+2] = gmul(col[0], 13) ^ gmul(col[1], 9) ^ gmul(col[2], 14) ^ gmul(col[3], 11)
                new_state[c*4+3] = gmul(col[0], 11) ^ gmul(col[1], 13) ^ gmul(col[2], 9) ^ gmul(col[3], 14)
            state = new_state
    return bytes(state)

def pkcs7_pad(data: bytes) -> bytes:
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([pad_len] * pad_len)

def pkcs7_unpad(data: bytes) -> bytes:
    if len(data) == 0 or len(data) % BLOCK_SIZE != 0:
        raise ValueError("Invalid block size.")
    pad_len = data[-1]
    if pad_len == 0 or pad_len > BLOCK_SIZE:
        raise ValueError("Decryption failed: Padding not valid.")
    for b in data[-pad_len:]:
        if b != pad_len:
            raise ValueError("Decryption failed: Padding not valid.")
    return data[:-pad_len]

def encrypt_cbc(pt: bytes, iv: bytes) -> bytes:
    pt_padded = pkcs7_pad(pt)
    ct = bytearray()
    prev = iv
    for i in range(0, len(pt_padded), BLOCK_SIZE):
        block = pt_padded[i:i+BLOCK_SIZE]
        xored = bytes(b ^ p for b, p in zip(block, prev))
        enc = aes_encrypt_block(xored)
        ct.extend(enc)
        prev = enc
    return bytes(ct)

def decrypt_cbc(ct: bytes, iv: bytes) -> bytes:
    pt = bytearray()
    prev = iv
    for i in range(0, len(ct), BLOCK_SIZE):
        block = ct[i:i+BLOCK_SIZE]
        dec = aes_decrypt_block(block)
        xored = bytes(d ^ p for d, p in zip(dec, prev))
        pt.extend(xored)
        prev = block
    return pkcs7_unpad(bytes(pt))

def padding_oracle(iv: bytes, ct: bytes) -> bool:
    try:
        decrypt_cbc(ct, iv)
        return True
    except ValueError:
        return False

class PaddingOracleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Padding Oracle Attack Showcase")
        self.root.geometry("1100x700") 
        self.iv = bytearray()
        self.ct = bytearray()
        self.pt = bytearray()
        self.is_attacking = False
        self.setup_ui()

    def setup_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Phase 1: Server/Client Comm")
        self.notebook.add(self.tab2, text="Phase 2: Padding Oracle Attack")
        self.build_phase_1()
        self.build_phase_2()

    def build_phase_1(self):
        frame = ttk.LabelFrame(self.tab1, text="Server: Prepare Token")
        frame.pack(fill="x", padx=10, pady=10)
        ttk.Label(frame, text="Plaintext:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.pt_entry = ttk.Entry(frame, width=50)
        self.pt_entry.insert(0, "SECRET")
        self.pt_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame, text="IV (Hex) [Optional]:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.iv_entry = ttk.Entry(frame, width=50)
        self.iv_entry.insert(0, os.urandom(BLOCK_SIZE).hex())
        self.iv_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Encrypt & Create Token", command=self.encrypt_token).grid(row=2, column=0, columnspan=2, pady=10)
        self.log_text = tk.Text(self.tab1, height=15, width=100, state='disabled', font=("Courier", 10))
        self.log_text.pack(padx=10, pady=5)
        client_frame = ttk.LabelFrame(self.tab1, text="Client: Send Token to Server")
        client_frame.pack(fill="x", padx=10, pady=10)
        ttk.Button(client_frame, text="Send Token (Bad Padding)", command=self.send_bad_padding).pack(side="left", padx=20, pady=10)
        ttk.Button(client_frame, text="Send Token (Good Padding)", command=self.send_good_padding).pack(side="right", padx=20, pady=10)

    def log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def encrypt_token(self):
        pt_str = self.pt_entry.get()
        iv_hex = self.iv_entry.get()
        if not pt_str or not iv_hex:
            messagebox.showerror("Error", "Please provide Plaintext and IV.")
            return
        try:
            self.iv = bytes.fromhex(iv_hex)
            if len(self.iv) != BLOCK_SIZE:
                self.iv = os.urandom(BLOCK_SIZE)
                self.iv_entry.delete(0, tk.END)
                self.iv_entry.insert(0, self.iv.hex())
        except ValueError:
            messagebox.showerror("Error", "Invalid IV Hex.")
            return
        self.pt = pt_str.encode()
        self.ct = encrypt_cbc(self.pt, self.iv)
        self.log("--- ENCRYPTION COMPLETE ---")
        self.log(f"Plaintext (Padded): {pkcs7_pad(self.pt).hex()}")
        self.log(f"Packet Format: [ IV || Ciphertext ]")
        self.log(f"Packet Built : {self.iv.hex()} || {self.ct.hex()}")
        self.log("Ready to simulate client interactions.\n")

    def send_bad_padding(self):
        if not self.ct: return
        tampered_iv = bytearray(self.iv)
        tampered_iv[-1] ^= 0xFF
        self.log(">> Client sending Token with TAMPERED IV (Bad Padding)...")
        self.log("<< Server Response: 500 Internal Error (Decryption failed: Padding not valid)\n")

    def send_good_padding(self):
        if not self.ct: return
        self.log(">> Client sending Original Token (Good Padding)...")
        is_valid = padding_oracle(self.iv, self.ct)
        if is_valid:
            self.log("<< Server Response: 200 OK (Serialization failed / Business logic err, but padding valid)\n")

    def build_phase_2(self):
        header = ttk.Frame(self.tab2)
        header.pack(fill="x", padx=10, pady=5)
        self.lbl_orig_pt = ttk.Label(header, text="Input Text: N/A", font=("Courier", 10, "bold"))
        self.lbl_orig_pt.pack(anchor="w")
        self.lbl_orig_iv = ttk.Label(header, text="Original IV: N/A", font=("Courier", 10, "bold"))
        self.lbl_orig_iv.pack(anchor="w")
        self.lbl_orig_ct = ttk.Label(header, text="Cipher Text: N/A", font=("Courier", 10, "bold"))
        self.lbl_orig_ct.pack(anchor="w")
        ttk.Separator(self.tab2, orient='horizontal').pack(fill='x', pady=10)
        display_frame = ttk.Frame(self.tab2)
        display_frame.pack(fill="both", expand=True, padx=10)
        self.lbl_flow = ttk.Label(display_frame, text="CT -> Block Decryption -> Dk", font=("Courier", 11, "bold"))
        self.lbl_flow.pack(pady=5)
        placeholder = "[ " + "?? "*16 + "]"
        self.var_dk = tk.StringVar(value=f"Dk Output (Intermed.):  {placeholder}")
        self.var_iv_prime = tk.StringVar(value=f"Bruteforce Block IV':   {placeholder}")
        self.var_pt = tk.StringVar(value=f"Clear Text Bytes (Pt):  {placeholder}")
        self.var_status = tk.StringVar(value="Requests: 0 | Current Guess: 0x00")
        ttk.Label(display_frame, textvariable=self.var_dk, font=("Courier", 12), foreground="blue").pack(pady=2, anchor="w")
        ttk.Label(display_frame, textvariable=self.var_iv_prime, font=("Courier", 12), foreground="red").pack(pady=2, anchor="w")
        ttk.Label(display_frame, textvariable=self.var_pt, font=("Courier", 12), foreground="green").pack(pady=2, anchor="w")
        ttk.Label(display_frame, textvariable=self.var_status, font=("Courier", 12, "bold")).pack(pady=15)
        self.btn_attack = ttk.Button(self.tab2, text="Start Padding Oracle Attack", command=self.start_attack)
        self.btn_attack.pack(pady=10)

    def format_bytearray(self, arr: bytearray, missing_idx: int = -1) -> str:
        res = []
        for i in range(BLOCK_SIZE):
            if i <= missing_idx: res.append("??")
            else: res.append(f"{arr[i]:02x}")
        return "[ " + " ".join(res) + " ]"

    def start_attack(self):
        if not self.ct:
            messagebox.showerror("Error", "Go to Phase 1 and generate a token first.")
            return
        if self.is_attacking: return
        self.is_attacking = True
        self.btn_attack.config(state='disabled')
        self.lbl_orig_pt.config(text=f"Input Text: {self.pt.decode('utf-8', errors='ignore')} ({self.pt.hex()})")
        self.lbl_orig_iv.config(text=f"Original IV: {self.iv.hex()}")
        self.lbl_orig_ct.config(text=f"Cipher Text: {self.ct.hex()}")
        self.current_block_idx = 0
        self.total_blocks = len(self.ct) // BLOCK_SIZE
        self.full_decrypted_pt = bytearray()
        self.requests = 0
        self.prepare_block_attack()

    def prepare_block_attack(self):
        if self.current_block_idx >= self.total_blocks:
            self.finish_attack()
            return
        if self.current_block_idx == 0: self.current_block_iv = self.iv
        else:
            start = (self.current_block_idx - 1) * BLOCK_SIZE
            self.current_block_iv = self.ct[start : start + BLOCK_SIZE]
        start_ct = self.current_block_idx * BLOCK_SIZE
        self.target_ct_block = self.ct[start_ct : start_ct + BLOCK_SIZE]
        self.attack_byte_idx = BLOCK_SIZE - 1
        self.attack_guess = 0
        self.found_dk = bytearray(BLOCK_SIZE)
        self.found_pt = bytearray(BLOCK_SIZE)
        self.root.after(10, self.attack_step)

    def attack_step(self):
        if self.attack_byte_idx < 0:
            self.full_decrypted_pt.extend(self.found_pt)
            self.current_block_idx += 1
            self.prepare_block_attack()
            return
        pad_val = BLOCK_SIZE - self.attack_byte_idx
        iv_prime = bytearray(BLOCK_SIZE)
        for i in range(self.attack_byte_idx + 1, BLOCK_SIZE):
            iv_prime[i] = self.found_dk[i] ^ pad_val
        iv_prime[self.attack_byte_idx] = self.attack_guess
        self.requests += 1
        is_valid = padding_oracle(bytes(iv_prime), self.target_ct_block)
        self.var_iv_prime.set(f"Bruteforce Block IV':   {self.format_bytearray(iv_prime, -1)}")
        self.var_status.set(f"Block {self.current_block_idx+1}/{self.total_blocks} | Byte {self.attack_byte_idx} | Guess: 0x{self.attack_guess:02x} | Req: {self.requests}")
        if is_valid:
            dk_val = self.attack_guess ^ pad_val
            pt_val = dk_val ^ self.current_block_iv[self.attack_byte_idx]
            self.found_dk[self.attack_byte_idx] = dk_val
            self.found_pt[self.attack_byte_idx] = pt_val
            self.var_dk.set(f"Dk Output (Intermed.):  {self.format_bytearray(self.found_dk, self.attack_byte_idx - 1)}")
            self.var_pt.set(f"Clear Text Bytes (Pt):  {self.format_bytearray(self.found_pt, self.attack_byte_idx - 1)}")
            self.attack_byte_idx -= 1
            self.attack_guess = 0
            self.root.after(100, self.attack_step)
        else:
            self.attack_guess += 1
            if self.attack_guess > 255:
                self.attack_guess = 0
                self.attack_byte_idx -= 1 
            self.root.after(1, self.attack_step)

    def finish_attack(self):
        self.is_attacking = False
        self.btn_attack.config(state='normal')
        try:
            final_text = pkcs7_unpad(self.full_decrypted_pt).decode('utf-8', errors='ignore')
            self.var_status.set(f"Attack Complete! Total Requests: {self.requests}\nDecrypted Text: '{final_text}'")
        except Exception as e:
            self.var_status.set(f"Attack Finished, but Unpadding Failed: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PaddingOracleApp(root)
    root.mainloop()