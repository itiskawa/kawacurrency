import block, hashlib


class Blockchain:

    def __init__(self):
        self.chain = [] # the chain of blocks
        self.current_data = [] # ledger of transactions
        self.nodes = set()
        self.construct_genesis() # creates initial Block
