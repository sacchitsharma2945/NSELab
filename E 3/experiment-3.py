import hashlib
import time
import random

shared_secret = "network_secret_key"

def generate_nonce():
    return str(random.randint(100000, 999999))

def hash_response(nonce, secret):
    return hashlib.sha256((nonce + secret).encode()).hexdigest()

# Server: send nonce
nonce = generate_nonce()
print("Server sends nonce to client:", nonce)

# Client: compute response
client_response = hash_response(nonce, shared_secret)
print("Client sends encrypted response:", client_response)

# Server: verify response
expected_response = hash_response(nonce, shared_secret)
if client_response == expected_response:
    print("Authentication Successful")
else:
    print("Authentication Failed")

# --- Replay Attack Handling with Timestamp ---
timestamp = str(int(time.time()))
nonce_with_time = nonce + timestamp
response_with_time = hashlib.sha256((nonce_with_time + shared_secret).encode()).hexdigest()
print("Client sends response with timestamp:", response_with_time)

# Server: verify with timestamp freshness
current_time = int(time.time())
received_time = int(timestamp)

if abs(current_time - received_time) <= 5:
    expected_time_resp = hashlib.sha256((nonce + timestamp + shared_secret).encode()).hexdigest()
    if response_with_time == expected_time_resp:
        print("Authentication Successful with replay protection")
    else:
        print("Authentication Failed")
else:
    print("Replay attack detected - timestamp expired")
