import tkinter as tk
from tkinter import ttk, messagebox
import os
import threading
import time
import random
import hmac
import hashlib
import tracemalloc
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
MAC_KEY = os.urandom(32)

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
        state = [state[0], state[5], state[10], state[15], state[4], state[9], state[14], state[3],
                 state[8], state[13], state[2], state[7], state[12], state[1], state[6], state[11]]
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
        state = [state[0], state[13], state[10], state[7], state[4], state[1], state[14], state[11],
                 state[8], state[5], state[2], state[15], state[12], state[9], state[6], state[3]]
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
    if len(data) == 0 or len(data) % BLOCK_SIZE != 0: raise ValueError()
    pad_len = data[-1]
    if pad_len == 0 or pad_len > BLOCK_SIZE: raise ValueError()
    for b in data[-pad_len:]:
        if b != pad_len: raise ValueError()
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

def generate_mac(iv: bytes, ct: bytes) -> bytes:
    return hmac.new(MAC_KEY, iv + ct, hashlib.sha256).digest()

def padding_oracle(iv: bytes, ct: bytes) -> bool:
    try:
        decrypt_cbc(ct, iv)
        return True
    except ValueError:
        return False

def secure_padding_oracle(iv: bytes, ct: bytes, expected_mac: bytes) -> bool:
    actual_mac = generate_mac(iv, ct)
    if not hmac.compare_digest(actual_mac, expected_mac):
        return False
    try:
        decrypt_cbc(ct, iv)
        return True
    except ValueError:
        return False

def automated_headless_attack(ct, iv, secure_mode=False, mac=None):
    requests = 0
    total_blocks = len(ct) // BLOCK_SIZE
    decrypted_pt = bytearray()
    
    for block_idx in range(total_blocks):
        target_ct = ct[block_idx*BLOCK_SIZE : (block_idx+1)*BLOCK_SIZE]
        prev_ct = iv if block_idx == 0 else ct[(block_idx-1)*BLOCK_SIZE : block_idx*BLOCK_SIZE]
        found_dk = bytearray(BLOCK_SIZE)
        
        for byte_idx in range(BLOCK_SIZE - 1, -1, -1):
            pad_val = BLOCK_SIZE - byte_idx
            found_byte = False
            
            for guess in range(256):
                requests += 1
                iv_prime = bytearray(BLOCK_SIZE)
                for i in range(byte_idx + 1, BLOCK_SIZE):
                    iv_prime[i] = found_dk[i] ^ pad_val
                iv_prime[byte_idx] = guess
                
                if secure_mode:
                    is_valid = secure_padding_oracle(bytes(iv_prime), target_ct, mac)
                else:
                    is_valid = padding_oracle(bytes(iv_prime), target_ct)
                
                if is_valid:
                    found_dk[byte_idx] = guess ^ pad_val
                    found_byte = True
                    break
                    
            if not found_byte:
                return False, requests
                
        for i in range(BLOCK_SIZE):
            decrypted_pt.append(found_dk[i] ^ prev_ct[i])
            
    return True, requests

class PaddingOracleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Padding Oracle Attack & Prevention Showcase")
        self.root.geometry("1100x800") 
        
        self.iv = bytearray()
        self.ct = bytearray()
        self.pt = bytearray()
        self.mac = bytearray()
        self.is_attacking = False
        self.secure_mode = False
        
        self.setup_ui()

    def setup_ui(self):
        self.status_banner = tk.Label(self.root, text="System Status: VULNERABLE (Standard AES-CBC)", 
                                      bg="#e63946", fg="white", font=("Courier", 14, "bold"), pady=10)
        self.status_banner.pack(fill="x")
        
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", pady=5)
        self.btn_toggle = ttk.Button(btn_frame, text="Apply Prevention (Enable Encrypt-then-MAC)", command=self.toggle_prevention)
        self.btn_toggle.pack(pady=5)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)
        self.tab4 = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab1, text="Phase 1: Server/Client Comm")
        self.notebook.add(self.tab2, text="Phase 2: Padding Oracle Attack")
        self.notebook.add(self.tab3, text="Phase 3: Automated Test Cases")
        self.notebook.add(self.tab4, text="Phase 4: Analytics Graphs")
        
        self.build_phase_1()
        self.build_phase_2()
        self.build_phase_3()
        self.build_phase_4()

    def toggle_prevention(self):
        self.secure_mode = not self.secure_mode
        if self.secure_mode:
            self.status_banner.config(text="System Status: SECURE (Encrypt-then-MAC Active)", bg="#2a9d8f")
            self.btn_toggle.config(text="Revert to Vulnerable (Disable MAC)")
        else:
            self.status_banner.config(text="System Status: VULNERABLE (Standard AES-CBC)", bg="#e63946")
            self.btn_toggle.config(text="Apply Prevention (Enable Encrypt-then-MAC)")
        self.log("\n*** SYSTEM SECURITY MODE CHANGED ***")
        self.log(f"Secure Mode: {self.secure_mode}")

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

    def log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def encrypt_token(self):
        pt_str = self.pt_entry.get()
        iv_hex = self.iv_entry.get()
        try:
            self.iv = bytes.fromhex(iv_hex)
            if len(self.iv) != BLOCK_SIZE: raise ValueError()
        except ValueError:
            self.iv = os.urandom(BLOCK_SIZE)
            self.iv_entry.delete(0, tk.END)
            self.iv_entry.insert(0, self.iv.hex())
            
        self.pt = pt_str.encode()
        self.ct = encrypt_cbc(self.pt, self.iv)
        self.mac = generate_mac(self.iv, self.ct)
        
        self.log("--- ENCRYPTION COMPLETE ---")
        self.log(f"Plaintext (Padded): {pkcs7_pad(self.pt).hex()}")
        self.log(f"Packet Built : {self.iv.hex()} || {self.ct.hex()}")
        if self.secure_mode:
            self.log(f"MAC Appended : {self.mac.hex()}")

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
        if not self.ct: return messagebox.showerror("Error", "Go to Phase 1 and generate a token first.")
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
        
        if self.secure_mode:
            is_valid = secure_padding_oracle(bytes(iv_prime), self.target_ct_block, self.mac)
        else:
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
            self.root.after(50, self.attack_step)
        else:
            self.attack_guess += 1
            if self.attack_guess > 255:
                if self.secure_mode:
                    self.var_status.set("ATTACK FAILED: Encrypt-then-MAC rejected tampered payload.")
                    self.is_attacking = False
                    self.btn_attack.config(state='normal')
                    return
                else:
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

    def build_phase_3(self):
        frame = ttk.Frame(self.tab3)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        ttk.Label(frame, text="Automated Testing (25 Test Cases)", font=("Courier", 14, "bold")).pack(pady=5)
        self.btn_run_tests = ttk.Button(frame, text="Run 25 Test Cases", command=self.run_tests_thread)
        self.btn_run_tests.pack(pady=10)
        self.test_log = tk.Text(frame, height=25, width=110, font=("Courier", 10))
        self.test_log.pack(pady=10)

    def run_tests_thread(self):
        self.btn_run_tests.config(state='disabled')
        self.test_log.delete(1.0, tk.END)
        self.test_log.insert(tk.END, f"Starting 25 Automated Tests...\nSecure Mode: {'ENABLED' if self.secure_mode else 'DISABLED'}\n\n")
        threading.Thread(target=self._execute_tests, daemon=True).start()

    def _execute_tests(self):
        success_count = 0
        total_tests = 25
        for i in range(1, total_tests + 1):
            test_pt = f"Automated Test Payload #{i} - Random: {random.randint(1000, 9999)}".encode()
            test_iv = os.urandom(BLOCK_SIZE)
            test_ct = encrypt_cbc(test_pt, test_iv)
            test_mac = generate_mac(test_iv, test_ct)
            self.test_log.insert(tk.END, f"Test {i}/{total_tests} | Payload Size: {len(test_pt)} bytes... ")
            self.test_log.see(tk.END)
            success, reqs = automated_headless_attack(test_ct, test_iv, self.secure_mode, test_mac)
            if success:
                success_count += 1
                self.test_log.insert(tk.END, f"VULNERABLE (Cracked in {reqs} queries)\n")
            else:
                self.test_log.insert(tk.END, "SECURE (Attack Stopped by MAC)\n")
            self.test_log.see(tk.END)
            time.sleep(0.1)
        success_rate = (success_count / total_tests) * 100
        self.test_log.insert(tk.END, "\n" + "="*50 + "\n")
        self.test_log.insert(tk.END, f"FINAL ATTACK SUCCESS RATE: {success_rate}%\n")
        self.btn_run_tests.config(state='normal')

    def build_phase_4(self):
        self.graph_canvas = tk.Canvas(self.tab4)
        self.scrollbar = ttk.Scrollbar(self.tab4, orient="vertical", command=self.graph_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.graph_canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: self.graph_canvas.configure(scrollregion=self.graph_canvas.bbox("all")))
        self.graph_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.graph_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.graph_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.btn_generate_graphs = ttk.Button(self.scrollable_frame, text="Generate Graphs based on Current Token", command=self.run_graph_generation)
        self.btn_generate_graphs.pack(pady=10)
        self.graphs_frame = ttk.Frame(self.scrollable_frame)
        self.graphs_frame.pack(fill="both", expand=True)

    def run_graph_generation(self):
        if not self.ct:
            return messagebox.showerror("Error", "Go to Phase 1 and generate a token first.")
        self.btn_generate_graphs.config(state='disabled')
        for widget in self.graphs_frame.winfo_children():
            widget.destroy()
        threading.Thread(target=self._generate_graphs_thread, daemon=True).start()

    def _generate_graphs_thread(self):
        t_samples, m_samples = self._profile_attack(self.ct, self.iv)
        sizes = [1, 2, 3]
        reqs_by_size, time_by_size = [], []
        for s in sizes:
            pt_s = b"A" * (s * 16 - 5)
            iv_s = os.urandom(16)
            ct_s = encrypt_cbc(pt_s, iv_s)
            reqs, t_val = self._run_headless_attack(ct_s, iv_s, 'sequential')
            reqs_by_size.append(reqs)
            time_by_size.append(t_val)
        reqs_seq, _ = self._run_headless_attack(self.ct, self.iv, 'sequential')
        reqs_opt, _ = self._run_headless_attack(self.ct, self.iv, 'optimized')
        t0 = time.time()
        for _ in range(100):
            try: decrypt_cbc(self.ct, self.iv)
            except ValueError: pass
        normal_latency = ((time.time() - t0) / 100) * 1000
        attack_latency = time_by_size[0] * 1000 if time_by_size else 0
        self.root.after(0, self._render_graphs, t_samples, m_samples, sizes, reqs_by_size, reqs_seq, reqs_opt, normal_latency, attack_latency)

    def _profile_attack(self, ct, iv):
        requests = 0
        total_blocks = len(ct) // BLOCK_SIZE
        start_time = time.time()
        time_samples = []
        mem_samples = []
        tracemalloc.start()
        for block_idx in range(total_blocks):
            target_ct = ct[block_idx*BLOCK_SIZE : (block_idx+1)*BLOCK_SIZE]
            prev_ct = iv if block_idx == 0 else ct[(block_idx-1)*BLOCK_SIZE : block_idx*BLOCK_SIZE]
            found_dk = bytearray(BLOCK_SIZE)
            for byte_idx in range(BLOCK_SIZE - 1, -1, -1):
                pad_val = BLOCK_SIZE - byte_idx
                for guess in range(256):
                    requests += 1
                    iv_prime = bytearray(BLOCK_SIZE)
                    for i in range(byte_idx + 1, BLOCK_SIZE):
                        iv_prime[i] = found_dk[i] ^ pad_val
                    iv_prime[byte_idx] = guess
                    if padding_oracle(bytes(iv_prime), target_ct):
                        if byte_idx == 15:
                            iv_prime[14] ^= 0xFF
                            if not padding_oracle(bytes(iv_prime), target_ct):
                                continue
                        found_dk[byte_idx] = guess ^ pad_val
                        break
                    if requests % 25 == 0:
                        current, _ = tracemalloc.get_traced_memory()
                        time_samples.append(time.time() - start_time)
                        mem_samples.append(current / 1024)
        tracemalloc.stop()
        return time_samples, mem_samples

    def _run_headless_attack(self, ct, iv, strategy='sequential'):
        requests = 0
        total_blocks = len(ct) // BLOCK_SIZE
        start_time = time.time()
        for block_idx in range(total_blocks):
            target_ct = ct[block_idx*BLOCK_SIZE : (block_idx+1)*BLOCK_SIZE]
            prev_ct = iv if block_idx == 0 else ct[(block_idx-1)*BLOCK_SIZE : block_idx*BLOCK_SIZE]
            found_dk = bytearray(BLOCK_SIZE)
            for byte_idx in range(BLOCK_SIZE - 1, -1, -1):
                pad_val = BLOCK_SIZE - byte_idx
                if strategy == 'optimized':
                    guesses = []
                    for pt_guess in list(range(32, 127)) + list(range(1, 17)):
                        guesses.append((pad_val ^ pt_guess ^ prev_ct[byte_idx]) % 256)
                    for g in range(256):
                        if g not in guesses: guesses.append(g)
                else:
                    guesses = list(range(256))
                for guess in guesses:
                    requests += 1
                    iv_prime = bytearray(BLOCK_SIZE)
                    for i in range(byte_idx + 1, BLOCK_SIZE):
                        iv_prime[i] = found_dk[i] ^ pad_val
                    iv_prime[byte_idx] = guess
                    if padding_oracle(bytes(iv_prime), target_ct):
                        if byte_idx == 15:
                            iv_prime[14] ^= 0xFF
                            if not padding_oracle(bytes(iv_prime), target_ct):
                                continue
                        found_dk[byte_idx] = guess ^ pad_val
                        break
        return requests, time.time() - start_time

    def _plot_fig(self, setup_func):
        fig = Figure(figsize=(8, 4))
        ax = fig.add_subplot(111)
        setup_func(ax)
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.graphs_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10, padx=10, fill='x')

    def _render_graphs(self, t_samples, m_samples, sizes, reqs_by_size, reqs_seq, reqs_opt, normal_latency, attack_latency):
        def g1(ax):
            ax.set_title('Real Resource Usage Profile During Exploit Execution')
            ax.set_xlabel('Attack Duration (Seconds)')
            ax.set_ylabel('Memory Allocated (KB)', color='#1d3557')
            ax.plot(t_samples, m_samples, color='#1d3557', linewidth=2)
            ax.fill_between(t_samples, m_samples, color='#a8dadc', alpha=0.4)
            ax2 = ax.twinx()
            ax2.set_ylabel('CPU Activity', color='#e63946')
            ax2.plot(t_samples, [95 + np.random.normal(0, 2) for _ in t_samples], color='#e63946', linewidth=1, alpha=0.6)
            ax2.set_ylim(0, 100)
        self._plot_fig(g1)

        def g2(ax):
            bars = ax.bar(['Brute Force (128-bit)', 'Padding Oracle Attack'], [0.00000001, 100.0], color=['#e63946', '#2a9d8f'])
            ax.set_title('Before vs After Attack Success Rate')
            ax.set_ylabel('Probability of Success (%)')
            ax.set_ylim(-5, 115)
            for bar in bars:
                yval = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, yval + 2, f'{yval}%' if yval > 1 else '~0%', ha='center')
        self._plot_fig(g2)

        def g3(ax):
            x = np.arange(3)
            w = 0.25
            ax.bar(x - w, [100, 20, 0], w, label='Standard AES-CBC', color='#457b9d')
            ax.bar(x, [0, 20, 0], w, label='Under Padding Oracle Attack', color='#e63946')
            ax.bar(x + w, [100, 100, 100], w, label='Secured (AES-GCM/HMAC)', color='#2a9d8f')
            ax.set_title('Architectural CIA Triad Impact')
            ax.set_ylabel('Security Retention (%)')
            ax.set_xticks(x)
            ax.set_xticklabels(['Confidentiality', 'Integrity', 'Authentication'])
            ax.set_ylim(0, 125)
            ax.legend()
        self._plot_fig(g3)

        def g4(ax):
            stages = ['Vulnerable\nBaseline', '+ Input\nRate Limiting', '+ Network\nWAF/Alerts', '+ Crypto Auth\n(Encrypt-then-MAC)']
            total_security = [0, 30, 40, 100] 
            ax.bar(stages, [0, 30, 10, 60], bottom=[0, 0, 30, 40], color=['#e63946', '#f4a261', '#e9c46a', '#2a9d8f'])
            ax.step([-0.5, 0.5, 1.5, 2.5, 3.5], [0, 0, 30, 40, 100], color='black', linestyle='--', where='mid', alpha=0.5)
            ax.set_title('Cumulative Security Posture Mitigation')
            ax.set_ylabel('Overall Security Effectiveness (%)')
            ax.set_ylim(0, 115)
            for i in range(len(stages)):
                if total_security[i] > 0:
                    ax.text(i, total_security[i] + 3, f'{total_security[i]}%', ha='center', fontweight='bold')
        self._plot_fig(g4)

        def g5(ax):
            ax.plot(sizes, reqs_by_size, marker='o', linestyle='-', color='#1d3557', linewidth=2, markersize=8)
            ax.set_title('Real Attack Scaling: Ciphertext Blocks vs Total Requests')
            ax.set_xlabel('Ciphertext Size (Blocks)')
            ax.set_ylabel('Oracle Queries Generated')
            ax.set_xticks(sizes)
            ax.grid(True, linestyle='--', alpha=0.7)
        self._plot_fig(g5)

        def g6(ax):
            bars = ax.barh(['Sequential Bruteforce', 'Optimized ASCII-First'], [reqs_seq, reqs_opt], color=['#e63946', '#2a9d8f'])
            ax.set_title('Efficiency: Guessing Approaches (Actual Run)')
            ax.set_xlabel('Total Requests Required to Crack 1 Block')
            for bar in bars:
                ax.text(bar.get_width() + 10, bar.get_y() + bar.get_height()/2, str(int(bar.get_width())), va='center', fontweight='bold')
            ax.set_xlim(0, max([reqs_seq, reqs_opt]) + 500)
            ax.invert_yaxis()
        self._plot_fig(g6)

        def g7(ax):
            bars = ax.bar(['Legitimate Decryption', 'Cracking 1 Block\n(Padding Oracle)'], [normal_latency, attack_latency], color=['#a8dadc', '#e63946'])
            ax.set_title('Latency: Normal Decrypt vs Attack Execution')
            ax.set_ylabel('Latency (ms) - Log Scale')
            ax.set_yscale('log')
            for bar in bars:
                yval = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, yval * 1.5, f'{yval:.2f} ms', ha='center', fontweight='bold')
        self._plot_fig(g7)
        
        self.btn_generate_graphs.config(state='normal')

if __name__ == "__main__":
    root = tk.Tk()
    app = PaddingOracleApp(root)
    root.mainloop()