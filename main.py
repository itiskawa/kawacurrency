import block, blockchain, transaction, time

blockchain = blockchain.Blockchain()

blockchain.construct_genesis()
print(blockchain)

blockchain.constructGenesis()

b = block.Block(1, transaction.Transaction("me", "you", 100, time.time), time-time)
blockchain.addBlock(b)

print(blockchain)