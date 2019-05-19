import hashlib
import json
from time import time


class Blockchain(object):
    def __init__(self):
        # this is to store all the blocks in the blockchain
        self.chain = []
        # this is to store the transactions
        self.currentTransactions = []

        # this is the first block
        self.new_block(previousHash=1, proof=100)

    def new_block(self, proof, previousHash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.currentTransactions,
            'proof': proof,
            'previousHash': previousHash or self.hash(self.chain[-1]),
        }
        # reset the current transactions list. This is how one block contains more than 1 transaction
        self.currentTransactions = []

        self.chain.append(block)

        return block

    def new_transaction(self, sender, recipient, amount):
        self.currentTransactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        # returning index of the next block which will hold this transaction
        return self.last_block['index'] + 1

    # with the use of staticmethod, function can be detached from the class and the instance
    @staticmethod
    def hash(block):
        # basic sha256 hashing
        blockString = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(blockString).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]
