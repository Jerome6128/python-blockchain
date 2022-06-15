import pytest
import time

from backend.blockchain.block import Block, GENESIS_DATA
from backend.config import MINE_RATE, SECONDS
from backend.util.hex_to_binary import hex_to_binary

def test_mine_block():
    last_block = Block.genesis()
    data = 'test_data'
    block = Block.mine_block(last_block, data)
    
    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_hash == last_block.hash
    assert hex_to_binary(block.hash)[:block.difficulty] == '0' * block.difficulty
    
    
def test_genesis():
    genesis = Block.genesis()
    
    assert isinstance(genesis, Block)
    
    for key, value in GENESIS_DATA.items():
        assert getattr(genesis, key) == value
        

def test_quickly_mined_block():
    last_block = Block.mine_block(Block.genesis(), 'foo')
    mined_block = Block.mine_block(last_block, 'bar')
    
    assert mined_block.difficulty == last_block.difficulty + 1
    

def test_slowly_mined_block():
    last_block = Block.mine_block(Block.genesis(), 'foo')
    time.sleep(MINE_RATE / SECONDS + 1)
    mined_block = Block.mine_block(last_block, 'bar')
    
    assert mined_block.difficulty == last_block.difficulty - 1


def test_mined_block_difficulty_limits_at_1():
    last_block = Block(
        time.time_ns(),
        'test_last_hash',
        'test_hash',
        'test_data',
        1,
        0
    )
    time.sleep(MINE_RATE / SECONDS + 1)
    mined_block = Block.mine_block(last_block, 'bar')
    
    assert mined_block.difficulty == last_block.difficulty


@pytest.fixture
def last_block():
    return Block.genesis()

@pytest.fixture
def block(last_block):
    return Block.mine_block(last_block, 'test_data')

def test_is_valid_block(last_block, block):
    Block.is_valid_block(last_block, block)
    
    
def test_is_valid_block_bad_last_hash(last_block, block):
    block.last_hash = 'evil_last_hash'
    
    with pytest.raises(Exception, match="The block last_hash must be correct"):
       Block.is_valid_block(last_block, block)


def test_is_valid_block_bad_proof_of_work(last_block, block):
    block.hash = 'evil_hash'
    
    with pytest.raises(Exception, match="The POW requirement was not met"):
       Block.is_valid_block(last_block, block)
       
       
def test_is_valid_block_jumped_difficulty(last_block, block):
    block.difficulty = last_block.difficulty + 2
    block.hash = f"{'0' * block.difficulty}111abc"
    
    with pytest.raises(Exception, match="The difficulty must only adjust by 1"):
       Block.is_valid_block(last_block, block)
       
def test_is_valid_block_bad_block_hash(last_block, block):
    block.hash =  f"{'0' * block.difficulty}111abc"

    with pytest.raises(Exception, match="The block hash must be a valid combination of the block fields"):
       Block.is_valid_block(last_block, block)