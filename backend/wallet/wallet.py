from encodings import utf_8
import uuid
import json

from backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import (
    encode_dss_signature,
    decode_dss_signature
)
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature


class Wallet:
    """
    An individual wallet for a miner.
    Keeps track of the miner's balance
    Allows a miner to authorize transactions
    """
    
    def __init__(self) -> None:
        self.address = str(uuid.uuid4())[0:8]
        self.balance = STARTING_BALANCE
        self.private_key = ec.generate_private_key(
            ec.SECP256K1(),
            default_backend()
            )
        self.public_key = self.private_key.public_key()
        self.serialize_public_key()
    
    def sign(self, data):
        """
        Generate a signature base on the data and local private key.
        """
        return decode_dss_signature(self.private_key.sign(
            json.dumps(data).encode('utf_8'),
            ec.ECDSA(hashes.SHA256())
            )
        )
    
    def serialize_public_key(self):
        """
        Reset the public key tto its serialized version
        """        
        self.public_key = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode("utf-8")
        
    
    @staticmethod
    def verify(data, public_key, signature):
        """
        Verify a signature based on the private key and data
        """
        deserialized_public_key = serialization.load_pem_public_key(
            public_key.encode('utf-8'),
            default_backend()
        )
        
        try:
            deserialized_public_key.verify(
                encode_dss_signature(*signature),
                json.dumps(data).encode('utf_8'),
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except InvalidSignature:
            return False

def main():
    wallet = Wallet()
    print(f'\nwallet.__dict__: {wallet.__dict__}')
    
    data = {'foo': 'bar'}
    signature = wallet.sign(data)
    print(f'\nsignature: {signature}')
    
    should_be_valid = Wallet.verify(data, wallet.public_key, signature)
    print(f"\nshould_be_valid: {should_be_valid}")
     
    should_be_invalid = Wallet.verify(data, Wallet().public_key, signature)
    print(f"\nshould_be_invalid: {should_be_invalid}")   
    
if __name__ == '__main__':
    main()