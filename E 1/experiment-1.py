import string

# Alphabets
lower, upper = string.ascii_lowercase, string.ascii_uppercase

# ---------- Caesar ----------
def caesar_encrypt(text, shift):
    res = ""
    for c in text:
        if c.islower():
            res += lower[(lower.index(c) + shift) % 26]
        elif c.isupper():
            res += upper[(upper.index(c) + shift) % 26]
        else:
            res += c
    return res

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

# ---------- Vigenere ----------
def vigenere_encrypt(text, key):
    res, j = "", 0
    for c in text:
        if c.isalpha():
            k = lower.index(key[j % len(key)].lower())
            if c.islower():
                res += lower[(lower.index(c) + k) % 26]
            else:
                res += upper[(upper.index(c) + k) % 26]
            j += 1
        else:
            res += c
    return res

def vigenere_decrypt(text, key):
    res, j = "", 0
    for c in text:
        if c.isalpha():
            k = lower.index(key[j % len(key)].lower())
            if c.islower():
                res += lower[(lower.index(c) - k) % 26]
            else:
                res += upper[(upper.index(c) - k) % 26]
            j += 1
        else:
            res += c
    return res

# ---------- Driver ----------
ch = input("1. Caesar\n2. Vigenere\nChoose: ")
msg = input("Enter text: ")

if ch == "1":
    s = int(input("Shift: "))
    enc = caesar_encrypt(msg, s)
    print("Encrypted:", enc)
    print("Decrypted:", caesar_decrypt(enc, s))
else:
    key = input("Key: ")
    enc = vigenere_encrypt(msg, key)
    print("Encrypted:", enc)
    print("Decrypted:", vigenere_decrypt(enc, key))
