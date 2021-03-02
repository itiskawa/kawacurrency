import hashlib, time
from block import *
from transaction import *

class Blockchain:

    def __init__(self):
        self.chain = [] # the chain of blocks
        self.pendingTransactions = [] # list of Transactions
        self.constructGenesis() # creates initial Block


    def constructGenesis(self):
        genesisTransaction = Transaction("me", "me", 50)
        genesis_block = Block(0, 0, [genesisTransaction])
        self.chain.append(genesis_block)


    def getLastBlock(self):
        if len(self.chain) > 0:
            return self.chain[-1]
        else:
            print("Error, the chain is empty!")



    def addBlock(self, blockToAdd):
        if len(self.chain) < 1:
            print("Unable to add a block to empty chain. It must be created first")
        
        print("Block Added \n")
        self.chain.append(blockToAdd)


    def makeTransaction(self, sender, receiver, amount):
        print("Transaction Made! \n")
        transaction = Transaction(sender, receiver, amount)
        self.pendingTransactions.append(transaction)



    def minePendingTransactions(self): # no miner for now
        if len(self.pendingTransactions) < 1:
            print("Error: cannot mine <1 transactions")
        
        #Block Creation & Mining process
        newBlock = Block(len(self.chain), self.getLastBlock().getHash(), self.pendingTransactions)
        # process continues if all transactions in Block are valid
        if newBlock.transactionsAreValid():
            newBlock.mine() # rat race moment

            print("Mining done")
            self.addBlock(newBlock)
            self.pendingTransactions = []
        else:
            print("Sorry, there are fraudy transactions in this list")




    def __str__(self):
        title = "Blockchain Status: \n \n"
        noBlocks = str(len(self.chain))
        

        return f"{title} The blockchain currently has {noBlocks} block(s) \n The last block's info is:\n {str(self.getLastBlock())} \n"


