from cryptography.fernet import Fernet

# Generate a new 32-byte base64 Fernet key
key = Fernet.generate_key()

# Save it to secret.key
with open("secret.key", "wb") as key_file:
    key_file.write(key)

print("secret.key generated successfully!")
