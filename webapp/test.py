import blockchain

blockchain = Blockchain()

print(str(blockchain))

#Making a Transaction
blockchain.makeTransaction("me", "you", 110)

# Actually mining the block 
blockchain.minePendingTransactions()

# total transaction of last block should be 110
print(str(blockchain))


blockchain.makeTransaction("John", "Emily", 20)
blockchain.makeTransaction("me", "you", 25)
blockchain.makeTransaction("him", "me", 47.4)

#should be same as last one
print(str(blockchain))

blockchain.minePendingTransactions()

# block number == 2 and transaction total should be 92.4
print(str(blockchain))
