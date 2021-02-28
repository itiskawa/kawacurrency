import block
"""
this class represents the blockchain itself. 
it
"""

class Blockchain:

    def __init__(self):
        self.chain = [] # the chain of blocks
        self.current_data = [] # ledger of transactions
        self.nodes = set()
        self.construct_genesis() # creates initial Block


    # constructs the first block of the chain, 
    # proof_no and prev_hash are set to zero
    def construct_genesis(self):
        self.construct_block(proof_no = 0, prev_hash = 0)


    # this methods constructs a block with given proof_no and previous hash
    # appends it to the chain & returns it
    def construct_block(proof_no, prev_hash):
        block = block.Block(index = len(self.chain), 
                            proof_no, 
                            prev_hash, 
                            data = self.current_data)

        # reset the data for next block
        self.current_data = []
        self.append_block(block)
        return block


    #simply appends desired block to the chain
    def append_block(self, block):
        self.chain.append(block)


    @staticmethod
    def check_validity(block, prev_block):

        if (block.index != prev_block.index + 1):
            return False

        elif prev_block.hash() != block.prev_hash:
            return False

        elif not Blockchain.verifying_proof(block.proof_no, prev_block.proof_no):
            return False
        
        elif block.timestamp <= prev_block.timestamp:
            return False

        return True
    
    def new_data(self, sender, recipient, quantity):
        self.current_data.append({
            'sender': sender,
            'recipient': recipient
            'quantity': quantity
        })
        return True

    @staticmethod
    def construct_proof_of_work(prev_proof):

        proof_no = 0
        while Blockchain.verifying_proof(proof_no, prev_proof) is False:
            proof_no += 1

        return proof_no

    @staticmethod
    def verifying_proof(prev_proof, proof):

        guess = f'{prev_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @property
    def lastBlock(self):
        return self.chain[-1]


