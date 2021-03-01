import hashlib

'''
Transaction class: 
Represents a transaction of the currency. Its info is:
    - the sender's ID / name
    - the receiver's ID / name
    - the amount (in native unit)
    - the timestamp (time at which transaction was requested)
'''
class Transaction:
    def __init__(self, sender, receiver, amt, timestamp):
        self.sender = sender
        self.receiver = receiver
        self.amt = amt
        self.timestamp = timestamp


        '''
        Calculates the hash of all the information of the transaction
        Will be used to give to the Bloc it will be a part of 
        '''
        @property
        def calculatehash(self):
            trans = "{}{}{}{}".format(self.sender, self.receiver, self.amt, self.timestamp)

            return hashlib.sha256(trans.encode()).hexdigest()


        '''
        Classic __repr__ method
        '''
        def __repr__(self):
            return "{}-{}-{}-{}".format(self.sender, self.receiver, 
                                        self.amt,
                                        self.timestamp)
