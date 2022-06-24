from backend.blockchain.blockchain import Blockchain
from backend.config import STARTING_BALANCE
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool
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
      
def test_calculate_balance():
    blockchain = Blockchain()
    wallet = Wallet()
    
    assert Wallet.calculate_balance(blockchain, wallet.address) == STARTING_BALANCE
    
    transaction_pool = TransactionPool()
    
    sent_amount = 10
    transaction = Transaction(wallet, Wallet().address, sent_amount)
    transaction_pool.set_transaction(transaction)
    blockchain.add_block(transaction_pool.transaction_data())
    transaction_pool.clear_blockchain_transactions(blockchain)
    
    assert Wallet.calculate_balance(blockchain, wallet.address) == STARTING_BALANCE - sent_amount
    
    received_amount = 95
    transaction = Transaction(Wallet(), wallet.address, received_amount)
    transaction_pool.set_transaction(transaction)
    blockchain.add_block(transaction_pool.transaction_data())
    transaction_pool.clear_blockchain_transactions(blockchain)
    
    assert Wallet.calculate_balance(blockchain, wallet.address) == STARTING_BALANCE - sent_amount + received_amount
    
    