# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 10:14:44 2025

@author: navee
"""

def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def caesar_decrypt(ciphertext, shift):
    return caesar_encrypt(ciphertext, -shift)

# Example usage
plaintext = "Hello Network Security"
shift = 3
ciphertext = caesar_encrypt(plaintext, shift)
print("Encrypted:", ciphertext)
print("Decrypted:", caesar_decrypt(ciphertext, shift))
