from backend.blockchain.block import Block

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
        

def main():
    blockchain = Blockchain()
    blockchain.add_block("one")
    blockchain.add_block("two")

    print(blockchain)

    print(f'blockchain.py __name__: {__name__}')    


if __name__ == '__main__':
    main()