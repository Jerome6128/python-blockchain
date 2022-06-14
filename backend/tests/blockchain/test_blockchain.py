from codecs import backslashreplace_errors
from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENESIS_DATA

def test_block_chain_instance():
    blockchain = Blockchain()
    assert blockchain.chain[0].hash == GENESIS_DATA['hash']
    

def test_add_block():
    blockchain = Blockchain()
    data = 'test_data'
    blockchain.add_block(data)
    
    assert blockchain.chain[-1].data == data
    
