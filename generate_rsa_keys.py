from Crypto.PublicKey import RSA

# Generate the first RSA key pair
key_pair_1 = RSA.generate(2048)
public_key_1 = key_pair_1.publickey()
private_key_1 = key_pair_1.export_key()

# Save the first key pair to files
with open("public_key_1.pem", "wb") as f:
    f.write(public_key_1.export_key())
with open("private_key_1.pem", "wb") as f:
    f.write(private_key_1)

# Generate the second RSA key pair
key_pair_2 = RSA.generate(2048)
public_key_2 = key_pair_2.publickey()
private_key_2 = key_pair_2.export_key()

# Save the second key pair to files
with open("public_key_2.pem", "wb") as f:
    f.write(public_key_2.export_key())
with open("private_key_2.pem", "wb") as f:
    f.write(private_key_2)
