import secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Generate a random secret key (AES256 needs 32 bytes)
key = secrets.token_bytes(32)

# Encrypt a message
nonce = secrets.token_bytes(12)  # GCM mode needs 12 fresh bytes every time
ciphertext = nonce + AESGCM(key).encrypt(nonce, b"Message", b"")

# Decrypt (raises InvalidTag if using wrong key or corrupted ciphertext)
msg = AESGCM(key).decrypt(ciphertext[:12], ciphertext[12:], b"")
