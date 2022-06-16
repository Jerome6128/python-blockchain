import os
import time

from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from dotenv import load_dotenv

from backend.blockchain.block import Block


pnconfig = PNConfiguration()

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..') 
dotenv_path = os.path.join(PROJECT_ROOT, '.env')
load_dotenv(dotenv_path)

pnconfig.publish_key = os.environ.get('PUBLISH_KEY')
pnconfig.subscribe_key = os.environ.get('SUBSCRIBE_KEY')


CHANNELS = {
    'TEST'  : 'TEST',
    'BLOCK' : 'BLOCK'
}


class Listener(SubscribeCallback):
    def __init__(self, blockchain) -> None:
        self.blockchain = blockchain
    
    def message(self, pubnub, message_object):
        print(f'\n-- Channel: {message_object.channel} | Message: {message_object.message}')
        
        if message_object.channel == CHANNELS['BLOCK']:
            block = Block.from_json(message_object.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)
            try:
                self.blockchain.replace_chain(potential_chain)
                print("\n -- Successfully replaced thee local chain")
            except Exception as e:
                print(f"\n -- Did no replace chain: {e}")
        

class PubSub():
    """
    Handles the publish/subscribe layer of the application
    Provides communication between the nodes of the blockchain network
    """

    def __init__(self, blockchain) -> None:
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain))
        
    def publish(self, channel, message):
        """
        Publish the message object to the channel
        """
        self.pubnub.publish().channel(channel).message(message).sync()
    
    def broadcast_block(self, block):
        """
        Broadcast a block object to all nodes
        """
        self.publish(CHANNELS['BLOCK'], block.to_json())
        
        
def main():
    pubsub = PubSub()
    time.sleep(1)
    
    message = {'foo': 'bar'}
    pubsub.publish(CHANNELS['TEST'], message)
    
    block = Block.genesis()
    pubsub.broadcast_block(block)

if __name__ == '__main__':
    main()

