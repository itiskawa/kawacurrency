import hashlib, time

'''
Transaction class: 
Represents a transaction of the currency. Its info is:
    - the sender's ID / name
    - the receiver's ID / name
    - the amount (in native unit)
    - the timestamp (time at which transaction was requested)
'''



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


