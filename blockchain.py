import block, hashlib


class Blockchain:

    def __init__(self):
        self.chain = [] # the chain of blocks
        self.current_data = [] # ledger of transactions
        self.nodes = set()
        self.construct_genesis() # creates initial Block


    # constructs the first block of the chain, 
    # proof_no and prev_hash are set to zero
    def construct_genesis(self):
        self.construct_block(0, 0)


    # this methods constructs a block with given proof_no and previous hash
    # appends it to the chain & returns it
    def construct_block(self, proof_no, prev_hash):
        block1 = block.Block(id = len(self.chain), 
                            proof_no = proof_no, 
                            prev_hash = prev_hash, 
                            data = self.current_data)

        # reset the data for next block
        self.current_data = []
        self.append_block(block1)
        return block1


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
            'recipient': recipient,
            'quantity': quantity
        })
        return True

    @staticmethod
    def proof_of_work(prev_proof):

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

    def block_mining(self, miner_details):
        self.new_data(sender="0", 
                       receiver= miner_details, 
                        quantity = 1)

        last_block = self.lastBlock()

        last_proof_no = last_block.proof_no
        proof_no = self.proof_of_work(last_proof_no)

        last_hash = last_block.hash
        block = self.construct_block(proof_no, last_hash)

        return vars(block)


    def create_node(self, address):
        self.nodes.add(address)
        return True

    @staticmethod
    def obtain_block_object(block_data):
        #obtains block object from the block data

        return Block(
            block_data['index'],
            block_data['proof_no'],
            block_data['prev_hash'],
            block_data['data'],
            timestamp=block_data['timestamp'])