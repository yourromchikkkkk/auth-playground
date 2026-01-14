from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

# TODO: think of a better way to store the keys
def generate_asymmetric_keys(path: str = "keys") -> None:
    os.makedirs(path, exist_ok=True)

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(f"{path}/public.pem", "wb") as file:
        file.write(public_pem)
        print("Public key saved to keys/public.pem")

    with open(f"{path}/private.pem", "wb") as file:
        file.write(private_pem)
        print("Private key saved to keys/private.pem")