from OpenSSL import crypto
from socket import gethostname

CERT_FILE = "self-signed.crt"
KEY_FILE = "private.key"


class CertificateAuthority:

    @staticmethod
    def cert_gen(
            key,
            email_address="emailAddress",
            common_name="commonName",
            country_name="TUN",
            locality_name="localityName",
            state_or_province_name="stateOrProvinceName",
            organization_name="organizationName",
            organization_unit_name="organizationUnitName",
            serial_number=0,
            validity_end_in_seconds=10 * 365 * 24 * 60 * 60,
            certificate_location="self-signed.crt",
    ):
        # can look at generated file using openssl:
        # openssl x509 -inform pem -in self-signed.crt -noout -text
        # create a key pair
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 4096)
        # create a self-signed cert
        cert = crypto.X509()
        cert.get_subject().C = country_name
        cert.get_subject().ST = state_or_province_name
        cert.get_subject().L = locality_name
        cert.get_subject().O = organization_name
        cert.get_subject().OU = organization_unit_name
        cert.get_subject().CN = common_name
        cert.get_subject().emailAddress = email_address
        cert.set_serial_number(serial_number)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(validity_end_in_seconds)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha512')
        with open(certificate_location, "wt") as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))

    @staticmethod
    def create_self_signed_cert():
        # create a key pair
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 4096)

        # create a self-signed cert
        cert = crypto.X509()
        cert.get_subject().C = "TUN"
        cert.get_subject().ST = "Tunis"
        cert.get_subject().L = "Tunis"
        cert.get_subject().O = "INSAT"
        cert.get_subject().OU = "INSAT"
        cert.get_subject().CN = gethostname()
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha256')

        with open(CERT_FILE, "w") as f:
            f.write(
                crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
        with open(KEY_FILE, "w") as f:
            f.write(
                crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf-8"))
