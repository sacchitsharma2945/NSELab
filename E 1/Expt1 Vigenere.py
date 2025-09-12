# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 10:15:26 2025

@author: navee
"""

def vigenere_encrypt(text, key):
    result = ""
    key_length = len(key)
    key_int = [ord(i.lower()) - ord('a') for i in key]
    for i, char in enumerate(text):
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            offset = key_int[i % key_length]
            result += chr((ord(char) - base + offset) % 26 + base)
        else:
            result += char
    return result

def vigenere_decrypt(ciphertext, key):
    result = ""
    key_length = len(key)
    key_int = [ord(i.lower()) - ord('a') for i in key]
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            offset = key_int[i % key_length]
            result += chr((ord(char) - base - offset) % 26 + base)
        else:
            result += char
    return result

# Example usage
plaintext = "Network Security"
key = "key"
ciphertext = vigenere_encrypt(plaintext, key)
print("Encrypted:", ciphertext)
print("Decrypted:", vigenere_decrypt(ciphertext, key))
