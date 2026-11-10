# -*- coding: utf-8 -*-
"""生成本地测试用自签名证书，包含 127.0.0.1 和本机局域网 IP。"""
import datetime
import ipaddress
import socket

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

KEY_PATH = "key.pem"
CERT_PATH = "cert.pem"

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()

local_ip = get_local_ip()
print(f"本机局域网 IP: {local_ip}")

key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

name = x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, "che-xing-tong-an-local"),
])

san = x509.SubjectAlternativeName([
    x509.DNSName("localhost"),
    x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
    x509.IPAddress(ipaddress.IPv4Address(local_ip)),
])

now = datetime.datetime.now(datetime.timezone.utc)
cert = (
    x509.CertificateBuilder()
    .subject_name(name)
    .issuer_name(name)
    .public_key(key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(now - datetime.timedelta(days=1))
    .not_valid_after(now + datetime.timedelta(days=825))
    .add_extension(san, critical=False)
    .sign(key, hashes.SHA256())
)

with open(KEY_PATH, "wb") as f:
    f.write(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ))

with open(CERT_PATH, "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print(f"证书已生成: {CERT_PATH}, {KEY_PATH}")
print(f"SAN 包含: localhost, 127.0.0.1, {local_ip}")