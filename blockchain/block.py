import hashlib
import time
from transaction import *
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
        block_string = str(self.__index) + str(self.__prevHash) + str(self.__transactions) + str(self.__timestamp)

        return hashlib.sha256(block_string.encode()).hexdigest()

    def transactionsAreValid(self):
        validity = True
        for transaction in self.__transactions:
            validity &= transaction.isValid()
        return validity

    def mine(self):
        #difficult-ass thing to do
        #TODO
        pass

    def __str__(self):
        total = 0
        for transaction in self.__transactions:
            total += transaction.getAmount()

        return f"Block number : {self.__index} \n previous hash : {self.__prevHash}, \n transaction total: {str(total)}" 