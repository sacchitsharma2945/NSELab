# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 23:51:22 2025

@author: navee
"""

import hashlib
import time
import random

shared_secret = "network_secret_key"

def generate_nonce():
    return str(random.randint(100000, 999999))

def hash_response(nonce, secret):
    return hashlib.sha256((nonce + secret).encode()).hexdigest()

# Server side: generate nonce
nonce = generate_nonce()
print("Server sends nonce to client:", nonce)

# Client side: compute response hash
client_response = hash_response(nonce, shared_secret)
print("Client sends encrypted response:", client_response)

# Server side: verify response
expected_response = hash_response(nonce, shared_secret)

if client_response == expected_response:
    print("Authentication Successful")
else:
    print("Authentication Failed")

# To handle replay attack: include timestamp

timestamp = str(int(time.time()))
nonce_with_time = nonce + timestamp
response_with_time = hashlib.sha256((nonce_with_time + shared_secret).encode()).hexdigest()
print("Client sends encrypted response with timestamp:", response_with_time)

# Server verifies timestamp freshness (e.g., within 5 seconds)
current_time = int(time.time())
received_time = int(timestamp)

if abs(current_time - received_time) <= 5:
    expected_response_time = hashlib.sha256((nonce + timestamp + shared_secret).encode()).hexdigest()
    if response_with_time == expected_response_time:
        print("Authentication Successful with replay protection")
    else:
        print("Authentication Failed")
else:
    print("Replay attack detected - timestamp expired")
