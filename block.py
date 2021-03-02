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

    def __init__(self, index, prevHash, transactions):
        self.__index = index
        self.__prevHash = prevHash
        self.__transactions = transactions
        self.__timestamp = time.time()
        self.__hash = self.computeHash()

    def getHash(self):
        return self.__hash

    def computeHash(self):
        block_string = "{}{}{}{}{}".format(self.index, self.hash, 
                                            self.prev_hash,
                                            self.data, self.timestamp)

        return hashlib.sha256(block_string.encode()).hexdigest()

    def transactionsAreValid(self):
        validity = True
        for transaction in self.__transactions:
            validity &= transaction.isValid()
        return validity

    def mine(self):
        #difficult-ass thing to do
        pass