from backend.util.crypto_hash import crypto_hash

def test_crypto_hash():
    # It should create the same hash with arguments in any order
    assert crypto_hash(1, [2], 'three') == crypto_hash([2], 1, 'three')
    # It should always return the same hash for given data
    assert crypto_hash('foo') == 'b2213295d564916f89a6a42455567c87c3f480fcd7a1c15e220f17d7169a790b'
    
