# Challenge-Response Authentication Demo
# Run each phase separately to demonstrate different concepts

import hashlib
import time
import random
import secrets

# Shared secret key (in real systems, this would be securely distributed)
SHARED_SECRET = "network_secret_key"

def simple_hash(message):
    """Simple hash function for demonstration"""
    return hashlib.sha256((message + SHARED_SECRET).encode()).hexdigest()

def generate_nonce():
    """Generate a random nonce"""
    return str(random.randint(100000, 999999))

print("="*60)
print("CHALLENGE-RESPONSE AUTHENTICATION DEMONSTRATION")
print("="*60)

# =============================================================================
# PHASE 1: Basic Success - Show working authentication
# =============================================================================
print("\n>>> PHASE 1: Basic Challenge-Response Authentication")
print("Demonstrating: Normal successful authentication")
print("-" * 50)

# Server generates nonce
server_nonce = generate_nonce()
print(f"1. Server generates nonce: {server_nonce}")

# Client computes response
client_response = simple_hash(server_nonce)
print(f"2. Client computes response: {client_response[:16]}...")

# Server verifies
expected_response = simple_hash(server_nonce)
if client_response == expected_response:
    print("3. Authentication Successful!")
else:
    print("3. Authentication Failed!")

input("\nPress Enter to continue to Phase 2...")

# =============================================================================
# PHASE 2: Replay Attack Without Freshness
# =============================================================================
print("\n>>> PHASE 2: Replay Attack (No Freshness)")
print("Demonstrating: How replay attacks work without freshness")
print("-" * 50)

# Simulate a system without nonce/timestamp (VULNERABLE)
FIXED_MESSAGE = "LOGIN"
print(f"1. System uses fixed message: '{FIXED_MESSAGE}'")

# Client computes response (this will always be the same!)
captured_response = simple_hash(FIXED_MESSAGE)
print(f"2. Client response: {captured_response[:16]}...")

# Simulate normal authentication
print("3. First authentication attempt:")
if captured_response == simple_hash(FIXED_MESSAGE):
    print("   Authentication Successful")

# Simulate attacker replaying the same response
print("4. Attacker replays the SAME response:")
replayed_response = captured_response  # Attacker copies the response
if replayed_response == simple_hash(FIXED_MESSAGE):
    print("   Authentication Successful (PROBLEM! Replay worked)")
else:
    print("   Authentication Failed")

print("⚠️  VULNERABILITY: Same response works every time!")

input("\nPress Enter to continue to Phase 3...")

# =============================================================================
# PHASE 3: Timestamp-Based Replay Protection
# =============================================================================
print("\n>>> PHASE 3: Timestamp-Based Replay Protection")
print("Demonstrating: Using timestamps to prevent replay attacks")
print("-" * 50)

def hash_with_timestamp(nonce, timestamp):
    """Hash function that includes timestamp"""
    message = nonce + timestamp + SHARED_SECRET
    return hashlib.sha256(message.encode()).hexdigest()

# Normal authentication with timestamp
nonce = generate_nonce()
current_time = str(int(time.time()))
print(f"1. Server nonce: {nonce}")
print(f"2. Current timestamp: {current_time}")

# Client creates response with timestamp
client_response_with_time = hash_with_timestamp(nonce, current_time)
print(f"3. Client response with timestamp: {client_response_with_time[:16]}...")

# Server verifies (should succeed)
print("4. Server verification (immediate):")
server_time = int(time.time())
message_time = int(current_time)

if abs(server_time - message_time) <= 5:  # 5 second window
    expected = hash_with_timestamp(nonce, current_time)
    if client_response_with_time == expected:
        print("    Authentication Successful (within time window)")
    else:
        print("   Authentication Failed (hash mismatch)")
else:
    print("   Authentication Failed (timestamp expired)")

# Simulate replay attack after delay
print("5. Simulating replay attack after 6 seconds...")
print("   Waiting 6 seconds...")
time.sleep(6)

# Try to replay the old response
print("6. Attacker replays old response:")
replay_time = int(time.time())
if abs(replay_time - message_time) <= 5:
    print("   Authentication would succeed")
else:
    print("   Replay attack detected - timestamp expired!")

input("\nPress Enter to continue to Phase 4...")

# =============================================================================
# PHASE 4: Nonce-Based Freshness
# =============================================================================
print("\n>>> PHASE 4: Nonce-Based Freshness")
print("Demonstrating: Using nonce tracking to prevent replay")
print("-" * 50)

# Server keeps track of used nonces
used_nonces = set()

def authenticate_with_nonce_tracking(nonce):
    """Authenticate and track used nonces"""
    if nonce in used_nonces:
        return False, "Nonce already used (replay detected)"
    
    # Add nonce to used set
    used_nonces.add(nonce)
    return True, "Authentication successful"

# First authentication
nonce1 = generate_nonce()
print(f"1. First authentication with nonce: {nonce1}")
success, message = authenticate_with_nonce_tracking(nonce1)
print(f"   Result: {message}")

# Second authentication with new nonce
nonce2 = generate_nonce()
print(f"2. Second authentication with nonce: {nonce2}")
success, message = authenticate_with_nonce_tracking(nonce2)
print(f"   Result: {message}")

# Try to replay first nonce (should fail)
print(f"3. Attacker tries to replay first nonce: {nonce1}")
success, message = authenticate_with_nonce_tracking(nonce1)
print(f"   Result:  {message}")

print(f"4. Used nonces so far: {used_nonces}")

input("\nPress Enter to continue to Phase 5...")

# =============================================================================
# PHASE 5: Mutual Authentication
# =============================================================================
print("\n>>> PHASE 5: Mutual Authentication")
print("Demonstrating: Both client and server authenticate each other")
print("-" * 50)

def compute_response(challenge, role):
    """Compute response with role to prevent reflection attacks"""
    message = f"{role}|{challenge}|{SHARED_SECRET}"
    return hashlib.sha256(message.encode()).hexdigest()

print("Step 1: Server authenticates Client")
print("-" * 30)

# Server challenges client
server_nonce = generate_nonce()
print(f"1. Server → Client: Challenge = {server_nonce}")

# Client responds 
client_response = compute_response(server_nonce, "CLIENT")
print(f"2. Client → Server: Response = {client_response[:16]}...")

# Server verifies client
expected_client_response = compute_response(server_nonce, "CLIENT")
client_authenticated = (client_response == expected_client_response)
print(f"3. Server verifies: {'Client authenticated' if client_authenticated else ' Client failed'}")

print("\nStep 2: Client authenticates Server")
print("-" * 30)

# Client challenges server
client_nonce = generate_nonce()
print(f"4. Client → Server: Challenge = {client_nonce}")

# Server responds
server_response = compute_response(client_nonce, "SERVER")
print(f"5. Server → Client: Response = {server_response[:16]}...")

# Client verifies server
expected_server_response = compute_response(client_nonce, "SERVER")
server_authenticated = (server_response == expected_server_response)
print(f"6. Client verifies: {' Server authenticated' if server_authenticated else ' Server failed'}")

print(f"\nFinal Result:")
if client_authenticated and server_authenticated:
    print("🎉 MUTUAL AUTHENTICATION SUCCESSFUL!")
    print("   Both parties have verified each other's identity")
else:
    print(" MUTUAL AUTHENTICATION FAILED!")

print("\n" + "="*60)
