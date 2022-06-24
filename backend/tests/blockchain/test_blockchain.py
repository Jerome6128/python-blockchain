import pytest

from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENESIS_DATA
from backend.tests.blockchain.test_block import block
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet

def test_block_chain_instance():
    blockchain = Blockchain()
    assert blockchain.chain[0].hash == GENESIS_DATA['hash']
    

def test_add_block():
    blockchain = Blockchain()
    data = 'test_data'
    blockchain.add_block(data)
    
    assert blockchain.chain[-1].data == data


@pytest.fixture
def blockchain_three_blocks():
    blockchain = Blockchain()
    
    for i in range(3):
        blockchain.add_block([Transaction(Wallet(), 'recipient', i).to_json()])  
        
    return blockchain  

def test_is_valid_chain(blockchain_three_blocks):
    Blockchain.is_valid_chain(blockchain_three_blocks.chain)
    

def test_is_valid_chain_bad_genesis(blockchain_three_blocks):
    
    blockchain_three_blocks.chain[0].data = "evil_genesis"
        
    with pytest.raises(Exception, match="The genesis block must be valid"):
       Blockchain.is_valid_chain(blockchain_three_blocks.chain)

    
def test_replace_chain(blockchain_three_blocks):
    blockchain = Blockchain()
    blockchain.replace_chain(blockchain_three_blocks.chain)
    
    assert blockchain.chain == blockchain_three_blocks.chain


def test_replace_chain_not_longer(blockchain_three_blocks):
    blockchain = Blockchain()
    
    with pytest.raises(Exception, match="Cannot replace. The incoming chain must be longer"):
        blockchain_three_blocks.replace_chain(blockchain.chain)
 
        
def test_replace_chain_not_valid(blockchain_three_blocks):
    blockchain = Blockchain()
    blockchain_three_blocks.chain[-1].data = "evil_data"
    
    with pytest.raises(Exception, match="Cannot replace. The incoming chain is invalid:"):
        blockchain.replace_chain(blockchain_three_blocks.chain)

def test_is_valid_transaction_chain(blockchain_three_blocks):
    Blockchain.is_valid_transaction_chain(blockchain_three_blocks.chain)
    
def test_is_valid_transaction_chain_duplicate_transaction(blockchain_three_blocks):
    transaction = Transaction(Wallet(), 'recipient', 10).to_json()
    blockchain_three_blocks.add_block([transaction, transaction])
    
    with pytest.raises(Exception, match="is not unique"):
        Blockchain.is_valid_transaction_chain(blockchain_three_blocks.chain)

def test_is_valid_transaction_chain_multiple_reward_transaction(blockchain_three_blocks):
    miner_wallet = Wallet()
    reward_transaction_1 = Transaction.reward_transaction(miner_wallet).to_json()
    reward_transaction_2 = Transaction.reward_transaction(miner_wallet).to_json()
    
    blockchain_three_blocks.add_block([reward_transaction_1, reward_transaction_2])
    
    with pytest.raises(Exception, match="There can be only one mining reward per block"):
        Blockchain.is_valid_transaction_chain(blockchain_three_blocks.chain)

def test_is_valid_transaction_chain_bad_transaction(blockchain_three_blocks):
    transaction = Transaction(Wallet(), 'recipient', 10)
    transaction.input['signature'] = Wallet().sign(transaction.output)
    blockchain_three_blocks.add_block([transaction.to_json()])
    
    with pytest.raises(Exception):
        Blockchain.is_valid_transaction_chain(blockchain_three_blocks.chain)
        
def test_is_valid_transaction_chain_bad_historic_balance(blockchain_three_blocks):
    wallet = Wallet()
    transaction = Transaction(wallet, 'recipient', 10)
    transaction.output[wallet.address] = 100000
    transaction.input['amount'] = 100010
    transaction.input['signature'] = wallet.sign(transaction.output)
    blockchain_three_blocks.add_block([transaction.to_json()])
    
    with pytest.raises(Exception, match="has invalid input amount"):
        Blockchain.is_valid_transaction_chain(blockchain_three_blocks.chain)