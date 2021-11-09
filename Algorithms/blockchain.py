import datetime, hashlib, json

class Blockchain:

    # 0 for no target, 64 for impossible!
    # default 4
    difficulty=4

    def __init__(self):
        self.difficulty=self.difficulty%65
        self.chain = []

    def create_block(self, data):
        prev_hash='0'*64
        if(self.chain!=[]):
            prev_hash=self.chain[-1]['hash']
        block = {'index': len(self.chain),
                 'nonce':0,
                 'timestamp': str(datetime.datetime.now()),
                 'data': data,
                 'prev_hash': prev_hash,
                 'hash':'0'*64}
        self.PoW(block)
        self.chain.append(block)
        return block

    def get_prev_block(self):
        return self.chain[-1]

    def PoW(self, block):
        while True:
            hash=self.hash_sha256(block.copy())
            if hash[:self.difficulty]=='0'*self.difficulty:
                block['hash']=hash
                return
            block['nonce']+=1

    def hash_sha256(self, block):
        del block['hash']
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_valid_chain(self):
        prev_block = self.chain[0]
        block_index = 1
        while block_index < len(self.chain):
            block = self.chain[block_index]
            if block['prev_hash'] != prev_block['hash']:
                return False
            block_hash=self.hash_sha256(block.copy())
            if block['hash'] != block_hash:
                return False
            if block['hash'][:self.difficulty] != '0'*self.difficulty:
                return False
            prev_block = block
            block_index += 1
        return True

def mine_block(blockchain, data):
    blockchain.create_block(data)
    print("New block mined!")

def show_chain(blockchain):
    for block in blockchain.chain:
        print(block)

def check_chain(blockchain):
    if(blockchain.chain==[]):
        print("No chain!")
    else:
        print(blockchain.is_valid_chain())

# controller
blockchain=Blockchain()
while True:
    user_input=input('>')
    if user_input=='?':
        show_chain(blockchain)
        continue
    if user_input=='!':
        check_chain(blockchain)
        continue
    if user_input=='<':
        break
    mine_block(blockchain, user_input)