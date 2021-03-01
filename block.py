import hashlib
import time

'''
this represents a Block in my simple blockchain
the block needs:
- an identification number
- all the transactions done in the block
- a previous hash
- a timestamp
- the data of the transaction
'''
class Block:

    def __init__(self, index, prev_hash, transactions, timestamp):
        self.index = index
        self.prev_hash = prev_hash
        self.transactions = transactions
        self.timestamp = timestamp
        self.hash = self.computehash()

    @property #makes it protected
    def computehash(self):
        block_string = "{}{}{}{}{}".format(self.index, self.hash, 
                                            self.prev_hash,
                                            self.data, self.timestamp)

        return hashlib.sha256(block_string.encode()).hexdigest()