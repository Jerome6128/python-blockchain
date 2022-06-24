import pytest
from backend.config import MINING_REWARD, MINING_REWARD_INPUT
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet

def test_transaction():
    sender_wallet = Wallet()
    recipient = 'recipient'
    amount = 50
    transaction = Transaction(sender_wallet, recipient, amount)
    
    assert transaction.output['recipient'] == amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance -  amount
    
    assert 'timestamp' in transaction.input
    assert transaction.input['amount'] == sender_wallet.balance
    assert transaction.input['address'] == sender_wallet.address
    assert transaction.input['public_key'] == sender_wallet.public_key
    
    assert Wallet.verify(
        transaction.output,
        transaction.input['public_key'],
        transaction.input['signature']
    )

def test_transaction_exceeds_balance():
    with pytest.raises(Exception, match="Amount exceeds balance"):
        Transaction(Wallet(), 'recipient', 1050)
    
def test_transaction_update_exceeds_balance():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, 'recipient_1', 500)
    
    with pytest.raises(Exception, match="Amount exceeds balance"):
        transaction.update(sender_wallet, 'recipient_2', 600)

def test_transaction_update():
    sender_wallet = Wallet()
    first_recipient = 'first_recipient'
    first_amount = 50
    transaction = Transaction(sender_wallet, first_recipient, first_amount)
    
    next_recipient = 'next_recipient'
    next_amount = 75
    transaction.update(sender_wallet, next_recipient, next_amount)
    
    assert transaction.output[next_recipient] == next_amount
    assert transaction.output[sender_wallet.address] == \
        sender_wallet.balance - first_amount - next_amount
    
    assert Wallet.verify(
        transaction.output,
        transaction.input['public_key'],
        transaction.input['signature']
    )
    
    
    to_first_again_amount = 130
    transaction.update(sender_wallet, first_recipient, to_first_again_amount)
    
    assert transaction.output[first_recipient] == first_amount + to_first_again_amount
    assert transaction.output[sender_wallet.address] == \
        sender_wallet.balance - first_amount - next_amount - to_first_again_amount
    
    assert Wallet.verify(
        transaction.output,
        transaction.input['public_key'],
        transaction.input['signature']
    )
    
def test_valid_transaction():
    sender_wallet = Wallet()
    recipient = 'recipient'
    amount = 50
    transaction = Transaction(sender_wallet, recipient, amount)
    Transaction.is_valid_transaction(transaction)
    
def test_valid_transaction_with_invalid_outputs():
    sender_wallet = Wallet()
    recipient = 'recipient'
    amount = 50
    transaction = Transaction(sender_wallet, recipient, amount)
    transaction.output[sender_wallet.address] = 9999
    
    with pytest.raises(Exception, match="Invalid transaction output values"):
       Transaction.is_valid_transaction(transaction)
       
def test_valid_transaction_with_invalid_signature():
    sender_wallet = Wallet()
    recipient = 'recipient'
    amount = 50
    transaction = Transaction(sender_wallet, recipient, amount)
    transaction.input['signature'] = Wallet().sign(transaction.output)
    
    with pytest.raises(Exception, match="Invalid transaction signature"):
       Transaction.is_valid_transaction(transaction)
    
def test_reward_transaction():
    miner_wallet = Wallet()
    transaction = Transaction.reward_transaction(miner_wallet)
    
    assert transaction.input == MINING_REWARD_INPUT
    assert transaction.output[miner_wallet.address] == MINING_REWARD

def test_valid_reward_transaction():
    miner_wallet = Wallet()
    transaction = Transaction.reward_transaction(miner_wallet)
    Transaction.is_valid_transaction(transaction)
    
def test_invalid_reward_transaction_extra_recipient():
    miner_wallet = Wallet()
    transaction = Transaction.reward_transaction(miner_wallet)
    transaction.output['extra_recipient'] = 60
    
    with pytest.raises(Exception, match='Invalid mining reward'):
        transaction.is_valid_transaction(transaction)
    
def test_invalid_reward_transaction_invalid_amount():
    miner_wallet = Wallet()
    transaction = Transaction.reward_transaction(miner_wallet)
    transaction.output[miner_wallet.address] = 60
    
    with pytest.raises(Exception, match='Invalid mining reward'):
        transaction.is_valid_transaction(transaction)