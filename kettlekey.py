import os

# Generate a random secret key
secret_key = os.urandom(24)

# Print the raw secret key
print("Raw Secret Key:", secret_key)

# Encode the secret key in a hexadecimal format
encoded_secret_key = secret_key.hex()

# Print the encoded secret key
print("Encoded Secret Key:", encoded_secret_key)
