import hashlib
import time

'''
this represents a Block in my simple blockchain
the block needs:
- an identification number
- a proof number
- a previous hash
- a timestamp
- the data of the transaction
'''
class Block:

    def __init__(self, id, proof_no, prev_hash, data, timestamp=None):
        self.id = id 
        self.proof_no = proof_no
        self.prev_hash = prev_hash
        self.data = data
        self.timestamp = timestamp or time.time

    @property #makes it protected
    def hash(self):
        block_string = "{}{}{}{}{}".format(self.id, self.proof_no, 
                                            self.prev_hash,
                                            self.data, self.timestamp)

        return hashlib.sha256(block_string.encode()).hexdigest()


    # like a ToString
    def __repr__(self):
        return "{}-{}-{}-{}-{}".format(self.id, self.proof_no, 
                                        self.prev_hash,
                                        self.data, self.timestamp)


