from backend.blockchain.block import Block
from backend.config import MINING_REWARD_INPUT
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet

class Blockchain:
    """
    Blockchain: a public ledger of tnrasactions
    Implemented as a list of blocks - data sets of transactions
    """
    
    def __init__(self) -> None:
        self.chain = [Block.genesis()]
        
        
    def add_block(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data))
        
        
    def __repr__(self) -> str:
        return f'Blockchain: {self.chain}'
    
    
    def replace_chain(self, chain):
        """
        Replace the local chain with the incoming one in the following applies:
            - the incoming chain is longer than the local one
            - the incoming chain is formatted properly
        """
        
        if len(self.chain) >= len(chain):
            raise Exception('Cannot replace. The incoming chain must be longer')
        
        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f'Cannot replace. The incoming chain is invalid: {e}')

        self.chain = chain
        
    def to_json(self):
        """
        Serialize the blockchain into a list of blocks
        """
        return [block.to_json() for block in self.chain]
    
    @staticmethod
    def from_json(chain_json):
        """
        Deserialize a listt of serialized blocks into a Blockchain instance
        The result will contain a chain list of Block instances
        """
        return [Block.from_json(block_json) for block_json in chain_json]
        
    
    @staticmethod
    def is_valid_chain(chain):
        """
        Validate the incoming chain:
        Enforce the following rules of the blockchain:
            - the chain must start with the genesis block
            - blocks must be formatted correctly
        """
        
        if chain[0] != Block.genesis():
            raise Exception('The genesis block must be valid')
        
        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i-1]
            Block.is_valid_block(last_block, block)
            
        Blockchain.is_valid_transaction_chain(chain)
        
    @staticmethod
    def is_valid_transaction_chain(chain):
        """
        Enforce the rules of a chain composed of block of transactions
        - Each transaction must only appear once in the chain
        - There can only be one mining reward per block
        _ Each transaction must be valid
        """
        transaction_ids = []
        for i in range(len(chain)):
            block = chain[i]
            has_mining_reward = False
            for transaction_json in block.data:
                transaction = Transaction.from_json(transaction_json)
                if transaction.id in transaction_ids:
                    raise Exception(f"Transaction {transaction.id} is not unique")
                
                transaction_ids.append(transaction.id)
        
                if transaction.input == MINING_REWARD_INPUT:
                    if has_mining_reward:
                        raise Exception(f"""There can be only one mining reward per block.
                                        Check block with hash: {block.hash}"""
                                        )
                    has_mining_reward = True
                
                else:
                    historic_blockchain = Blockchain()
                    historic_blockchain.chain = chain[:i]
                    historic_balance = Wallet.calculate_balance(
                        historic_blockchain,
                        transaction.input['address']
                    )
                    if historic_balance != transaction.input['amount']:
                        raise Exception(f"Transaction {transaction.id} has invalid input amount")
                
                Transaction.is_valid_transaction(transaction)
                    
                    
        

def main():
    blockchain = Blockchain()
    blockchain.add_block("one")
    blockchain.add_block("two")

    print(blockchain)

    print(f'blockchain.py __name__: {__name__}')    


if __name__ == '__main__':
    main()