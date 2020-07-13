import datetime
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.x509.oid import NameOID
from pydantic import BaseSettings
from pydantic.class_validators import validator
from pydantic.networks import IPvAnyAddress
from typer import confirm


class LootMarshalSettings(BaseSettings):
    host: IPvAnyAddress
    port: int
    debug: bool
    ssl: bool
    ssl_keyfile: Path
    ssl_certfile: Path
    workers: int
    handler: str

    @validator("port")
    def valid_port(cls, value):
        if not 0 < value <= 65535:
            raise ValueError("Invalid Port! Must be between 1 and 65535.")
        return value

    @validator("handler")
    def valid_handler(cls, value):
        handlers = ["azure"]
        if value.lower() not in handlers:
            raise ValueError(f"Invalid Handler! Must be {handlers}")
        return value

    @validator("ssl_keyfile")
    def valid_key(cls, value, values):
        if not values["ssl"]:
            return value

        try:
            with open(value, "rb") as key_file:
                private_key = serialization.load_pem_private_key(
                    key_file.read(), password=None, backend=default_backend()
                )
        except Exception as e:
            new_key = confirm(
                f"{e}\n\n[*] Keyfile not valid. Would you like to generate one?"
            )
            if not new_key:
                exit()

            from cryptography.hazmat.primitives.asymmetric import rsa

            key = rsa.generate_private_key(
                public_exponent=65537, key_size=2048, backend=default_backend()
            )

            with open(value, "wb") as f:
                f.write(
                    key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                        encryption_algorithm=serialization.NoEncryption(),
                    )
                )
        return value

    @validator("ssl_certfile")
    def valid_cert(cls, value, values):
        if not values["ssl"]:
            return value

        try:
            with open(value, "rb") as key_file:
                public_key = x509.load_pem_x509_certificate(
                    key_file.read(), backend=default_backend()
                )
        except Exception as e:
            new_cert = confirm(
                f"{e}\n\n[*] Certfile not valid. Would you like to generate one?"
            )
            if not new_cert:
                exit()

            key = serialization.load_pem_private_key(
                open(values["ssl_keyfile"], "rb").read(),
                password=None,
                backend=default_backend(),
            )

            subject = issuer = x509.Name(
                [
                    x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
                    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Washington"),
                    x509.NameAttribute(NameOID.LOCALITY_NAME, "Redmond"),
                    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "LootMarshal"),
                    x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
                ]
            )

            basic_contraints = x509.BasicConstraints(ca=True, path_length=0)
            cert = (
                x509.CertificateBuilder()
                .subject_name(subject)
                .issuer_name(issuer)
                .public_key(key.public_key())
                .serial_number(x509.random_serial_number())
                .not_valid_before(datetime.datetime.utcnow())
                .not_valid_after(
                    datetime.datetime.utcnow() + datetime.timedelta(days=30)
                )
                .add_extension(
                    x509.SubjectAlternativeName([x509.DNSName("localhost")]), False
                )
                .add_extension(basic_contraints, False)
                .sign(key, hashes.SHA256(), default_backend())
            )
            # Write our certificate out to disk.
            with open(value, "wb") as f:
                f.write(cert.public_bytes(serialization.Encoding.PEM))
        return value
