from backend.wallet.wallet import Wallet

def test_verify_valid_signature():
    wallet = Wallet()
    data = {'foo': 'bar'}
    signature = wallet.sign(data)
    
    assert Wallet.verify(data, wallet.public_key, signature)

def test_verify_invalid_signature():
    wallet = Wallet()
    data = {'foo': 'bar'}
    signature = wallet.sign(data)
    
    assert not Wallet.verify(data, Wallet().public_key, signature)
      