from OpenSSL import crypto
from socket import gethostname
import uuid
from Helpers.RSAHelper import RSAHelper
import core.consts as config

CERT_FILE = "self-signed.crt"
KEY_FILE = "private.key"


class CertificateAuthorityHelper:

    @staticmethod
    def create_certificate_from_req(
            username, certificate_request
    ):
        # can look at generated file using openssl:
        # openssl x509 -inform pem -in self-signed.crt-noout -text
        # create a key pair
        # create a self-signed cert
        k = RSAHelper.load_private_key(config.SERVER_KEY_PATH)
        cert = crypto.X509()
        cert.get_subject().C = certificate_request.get_subject().C
        cert.get_subject().ST = certificate_request.get_subject().ST
        cert.get_subject().L = certificate_request.get_subject().L
        cert.get_subject().O = certificate_request.get_subject().O
        cert.get_subject().OU = certificate_request.get_subject().OU
        cert.get_subject().CN = certificate_request.get_subject().CN
        cert.get_subject().emailAddress = certificate_request.get_subject().emailAddress
        cert.set_serial_number(int(uuid.uuid4()))
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(certificate_request.public_key())
        cert.sign(k, 'SHA-256')
        CertificateAuthorityHelper.save_certificate(config.CLIENTS_CERTIFICATES_DIRECTORY + f'{username}.crt', cert)
        return cert

    @staticmethod
    def create_self_signed_cert(private_key, email_address="emailAddress",
                                common_name="commonName",
                                country_name="TUN",
                                locality_name="localityName",
                                state_or_province_name="stateOrProvinceName",
                                organization_name="organizationName",
                                organization_unit_name="organizationUnitName",
                                serial_number=int(uuid.uuid4()),
                                validity_end_in_seconds=10 * 365 * 24 * 60 * 60, ):
        # create a key pair
        k = RSAHelper.load_private_key(config.SERVER_KEY_PATH)

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
        cert.set_pubkey(k.publickey().exportKey('PEM'))
        cert.sign(k, 'SHA-256')

        with open(CERT_FILE, "w") as f:
            f.write(
                crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))

    @staticmethod
    def save_certificate(certificate_location, certificate):
        try:
            with open(certificate_location, "wt") as f:
                f.write(crypto.dump_certificate(
                    crypto.FILETYPE_PEM, certificate).decode("utf-8"))
        except:
            return False

    @staticmethod
    def read_certificate(path):
        try:
            with open(path, 'rb') as f:
                certificate = crypto.load_certificate(
                    crypto.FILETYPE_PEM, f.read())
            return certificate
        except:
            return False

    @staticmethod
    def create_certificate_request(private_key):
        req = crypto.X509Req()
        req.get_subject().CN = "nodename"
        req.get_subject().countryName = "TN"
        req.get_subject().stateOrProvinceName = "TUNIS"
        req.get_subject().localityName = "l"
        req.get_subject().organizationName = "org"
        req.get_subject().organizationalUnitName = "org"

        req.set_pubkey(private_key.publickey().exportKey('PEM'))
        req.sign(private_key, 'SHA-256')

        return req
