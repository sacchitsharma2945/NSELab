import hashlib

def hash_file(filename):
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# Hardcoded file names
file1 = "file.txt"
file2 = "file1.txt"

hash1 = hash_file(file1)
hash2 = hash_file(file2)

print(f"SHA-256 Hash of '{file1}': {hash1}")
print(f"SHA-256 Hash of '{file2}': {hash2}")

# Integrity check
if hash1 == hash2:
    print("\n✅ Files are Identical (Integrity Verified)")
else:
    print("\n❌ Files are Different (Possible Tampering)")
