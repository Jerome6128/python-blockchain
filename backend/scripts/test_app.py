import requests
import time

from backend.wallet.wallet import Wallet

BASE_URL = 'http://127.0.0.1:5000'

def get_blockchain():
    return requests.get(f'{BASE_URL}/blockchain').json()

def get_blockchain_mine():
    return requests.get(f'{BASE_URL}/blockchain/mine').json()
    
def post_wallet_transact(recipient, amount):
    data = {
            "recipient": recipient,
            "amount": amount
            }
    return requests.post(f'{BASE_URL}/wallet/transact', json=data).json()

def get_wallet_info():
    return requests.get(f'{BASE_URL}/wallet/info').json()

start_blockchain = get_blockchain()
print(f'\nstart_blockchain: {start_blockchain}')

recipient = Wallet().address

post_wallet_tansact_1 = post_wallet_transact(recipient, 21)
print(f'\npost_wallet_tansact_1: {post_wallet_tansact_1}')

time.sleep(1)
post_wallet_tansact_2 = post_wallet_transact(recipient, 13)
print(f'\npost_wallet_tansact_2: {post_wallet_tansact_2}')

time.sleep(1)
mined_block = get_blockchain_mine()
print(f'\nmined_block: {mined_block}')

wallet_balance = get_wallet_info()
print(f'\nwallet_balance: {wallet_balance}')