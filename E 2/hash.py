# -*- coding: utf-8 -*-
"""
Created on Mon Aug 25 16:11:16 2025

@author: navee
"""

import hashlib

def hash_file(filename):
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# Hash the file
filename = "abc.txt"
file_hash = hash_file(filename)
print(f"SHA-256 Hash of '{filename}': {file_hash}")
