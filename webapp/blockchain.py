import hashlib, time
from flask_login import current_user
from webapp.models import User
from webapp import db

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


    def chainLength(self):
        return len(self.chain)


    def addBlock(self, blockToAdd):
        if len(self.chain) < 1:
            print("Unable to add a block to empty chain. It must be created first")
        
        print("Block Added \n")
        self.chain.append(blockToAdd)


    def makeTransaction(self, sender, receiver, amount):
        #print("Transaction Made! \n")
        transaction = Transaction(sender, receiver, amount)
        current_user.balance -= amount
        rec = User.query.filter_by(username = receiver).first()
        rec.balance += amount
        db.session.commit()
        """ print("sender's new balance: ", current_user.balance)
        print("receiver's balance: ", rec.balance) """
        self.pendingTransactions.append(transaction)

        return True


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
            current_user.balance += 50.0
            db.session.commit()
        else:
            print("Sorry, there are fraudy transactions in this list")




    def __str__(self):
        title = "Blockchain Status: \n \n"
        noBlocks = str(len(self.chain))
        

        return f"{title} The blockchain currently has {noBlocks} block(s) \n The last block's info is:\n {str(self.getLastBlock())} \n"




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
    
    def getIndex(self):
        return self.__index
    
    def getPrevHash(self):
        return self.__prevHash

    def getTransactionsTotal(self):
        total = 0
        for transaction in self.__transactions:
            total += transaction.getAmount()
        return total




# still needs a lot of security add-ons, but it should work for now without verification
class Transaction:
    def __init__(self, sender, receiver, amt):
        self.__sender = sender
        self.__receiver = receiver
        self.__amt = amt
        self.__timestamp = time.time()
        self.hash = self.calculateHash


        '''
        Calculates the hash of all the information of the transaction
        Will be used to give to the Bloc it will be a part of 
        '''
    
    def calculateHash(self):
        trans = self.__sender + self.__receiver + str(self.__amt) + str(self.__timestamp)

        return hashlib.sha256(trans.encode()).hexdigest()

    def getAmount(self):
        return self.__amt

    def isValid(self):
        """ if self.hash != self.calculateHash():
            print("Hash modified!")
            return False """
        if (self.__sender == self.__receiver):
            print("Cannot send to yourself")
            return False
        if (self.__amt < 0):
            return False
        return True




    '''
    Classic __str__ method
    '''
    def __str__(self):
        return f"Transaction: \nsender : {self.__sender}, \nreceiver : {self.__receiver}, \namount : {self.__amt}, \ntimestamp : {str(self.__timestamp)}"
