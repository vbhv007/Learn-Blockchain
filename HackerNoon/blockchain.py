import hashlib
import json
from time import time
from uuid import uuid4
from textwrap import dedent
from flask import Flask, jsonify


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

    def proof_of_work(self, lastProof):
        newProof = 0
        while(self.vaild_proof(lastProof, newProof) is False):
            newProof += 1

        return newProof

    @staticmethod
    def valid_proof(lastProof, newProof):
        guess = f'{lastProof}{newProof}'.encode()
        guessHash = hashlib.sha256(guess).hexdigest()

        return guessHash[:4] == "0000"

    # with the use of staticmethod, function can be detached from the class and the instance
    @staticmethod
    def hash(block):
        # basic sha256 hashing
        blockString = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(blockString).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]


# API stuff
app = Flask(__name__)

nodeIdentifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    return "Mining a new block"


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    return "Adding a new transaction"


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
