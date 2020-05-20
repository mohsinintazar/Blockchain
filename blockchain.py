# Module 1 - Create a Blockchain

# Import libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify

# Part-1 - Building a Blockchain

## Declaring Blockchain class
class Blockchain:
    
    ### Declaring init method to self initiate 
    def __init__(self):
        ### Now we need to initialize the chain which will be a list of
        ### different blocks which will be appended when we mine them
        self.chain = []
        
        ### Now we need to initialize the genesis block or first block of the
        ### blockchain, here it will accept two arguments the first is the 
        ### proof because each block will has it's own proof and a previous
        ### hash value and for both we require arbitary value and we assign
        ### proof = 1 and previous_hash = '0' and here we are assigning quotes
        ### because we are going to use SHA256 which can only accept strings.
        self.create_block(proof = 1, previous_hash = '0')
        
    ### Declaring the create_block method it will be able to create the genesis
    ### block and other mined blocks
    def create_block(self, proof, previous_hash):
        ### Declaring block which will be a dictionary
        ### To get the index we just need to get the length of the chain + 1
        ### To get the timestamp we use datetime library and it's datetime
        ### module to get the current time and we put it in string otherwise
        ### we will be having format issues when working with json format
        ### To get the proof of work we will create a function
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash
            }
        
        ### Now as the block is created we need to append it to the chain
        self.chain.append(block)
        
        ### Now we need to return this block in order to show it's information
        ### in the Postman
        return block
    
    ### Now to get the previous block we declare a method which will only accept
    ### self argument because we only need self.chain list which has the last
    ### index of chain
    def get_previous_block(self):
        return self.chain[-1]

    ### Now we need to create the proof_of_work method, here we will create a
    ### problem or puzzle for the miner to solve it mine a new block.
    ### Proof of work is a number which is hard to find but easy to verify,
    ### because it was easy to find then miner could have mined tons of blocks
    ### and it could have a less value
    ### This proof of work will accept two arguments, the first will be self
    ### because we apply this from the instance of the object that we created
    ### from the class.
    ### The second argument is previous proof, because in order to make that 
    ### problem that miners have to solve we will take into account the previous
    ### proof, so the previous proof is an element of the problem that miners
    ### will need to consider to find a new proof
    def proof_of_work(self, previous_proof):
        ### We need to initialize the new_proof at 1 because to solve the
        ### problem we need to increment this value by 1 at each itteration
        ### until we get the right proof, because we are solving the problem
        ### by trial and error approach
        new_proof = 1
        
        ### To check if the proof is right or not we need to initialize a new
        ### variable which we set to False, once we get the right proof we set
        ### this to True and we end the WHILE loop
        check_proof = False
        
        ### Now we initialize WHILE loop until the check_proof is False
        while check_proof is False:
            ### Here we introduce the problem which needs to be solved by miner
            ### We add str and encode it so if the 
            ### answer of the problem is 16 then str will make it '16' and
            ### encode will add character to make it SHA256 acceptable like b'16' 
            ### And as we are dealing with Hexadecimal so, we add hexdigest
            hash_operation = hashlib.sha256(str(new_proof**4 - previous_proof**4).encode()).hexdigest()
        
            ### Now set the 2nd part of puzzle where we declare that if the
            ### initial 5 digits are 00000 then set the check_proof to True
            ### otherwise increment new_proof by 1 and check again
            if hash_operation[:5] == '00000':
                check_proof = True
            else:
                new_proof += 1
        
        ### Now once we get the puzzle solved we return this new_proof, so it
        ### can be returned to the create_block method
        return new_proof
    
    ### Define a method to check if everything is fine in blockchain, first check
    ### if each block of the blockchain has correct proof of work by solving the
    ### problem to get a SHA256 value starting with 00000 leading zeros. Second we
    ### check that previous hash of each block is equal to the hash of its
    ### previous block.
    
    ### This method is going to take in a block and return SHA256 cryptographic
    ### hash of the block.
    def hash(self, block):
        ### Because each block of our blockchain is going to have a dictionary
        ### format so, first we will need to convert it to string through
        ### json lib which we imported earlier by dumps function. We don't
        ### use the str function to convert it to string because later we are
        ### going to use the json format and str will not return json format.
        ### So, we are going to introduce a new variable encoded_block which
        ### will return the exact SHA256 cryptographic value that can be accepted
        ### by the hashlib.sha256 library. Here we are going to set the sort_keys
        ### true so, that the dictionary can be sorted according to the index.
        
        encoded_block = json.dumps(block,sort_keys = True).encode()
        
        ### Now we pass the encoded block into the hashlib library to return a
        ### sha256 value and then convert it to hexadecimal by hexdigest method.
        return hashlib.sha256(encoded_block).hexdigest()
    
    ### Now this is the second step where we will be looping through all of the
    ### blocks to see if the chain is valid.
    def is_chain_valid(self, chain):
        ### Now to start the loop we are going to initialize the variables of
        ### the loop first so, we initialize the block index. As we are going to
        ### check the 'previous_hash' value of current block is equal to it's  
        ### previous block hash so, we will also need to initialize the previous 
        ### block variable that has the first block of the chain which we get
        ### by index 0 of the chain. Then at the end of the WHILE loop we will
        ### update the value of this previous block variable to be equal to the 
        ### new block that we are dealing with in the itteration of the loop.
        previous_block = chain[0]
        block_index = 1
        
        ### Now to start itterating WHILE loop we are going to set the condition
        ### that the block index should be less than the length of the chain.
        while block_index < len(chain):
            ### Now we check two things, first the hash is equal to the previous
            ### block hash and second the proof of work is valid.
            ### So, first we are going to get the current block and by setting
            ### the index of the chain to block_index which means we start from
            ### first block of the chain.
            block = chain[block_index]
            
            ### Now we set the conditional statement to check if the 'previous_hash'
            ### value is different than the hash value of previous block then
            ### we will return false because that means chain is not valid.
            if block['previous_hash'] != self.hash(previous_block):
                return False
            
            ### Now we do the check upon the problem if it is solved like the
            ### cryptographic value starts with leading 00000. So, we will take
            ### the previous proof from our variable 'previous_block' and then
            ### we take the current proof by taking the 'proof' key of the current
            ### block and then we will compute the hash operation between both.
            previous_proof = previous_block['proof']
            
            ### Now we take the current block proof
            proof = block['proof']
    
            hash_operation = hashlib.sha256(str(proof**4 - previous_proof**4).encode()).hexdigest()
            
            if hash_operation[:5] != '00000':
                return False
            
            ### Now we need to update our looping variables, so, now the previous
            ### block will become our current block and we will also increment
            ### block_index by 1.
            previous_block = block
            block_index += 1
            
        ### Finally if everything went well then we will return true in the loop
        return True
    
# Part-2 - Mining our Blockchain

## 1 - Creating Web App
### Creating the Flask web application
app = Flask(__name__)
    
## 2 - Creating a Blockchain
### Creating an instance of the Blockchain class which we created in part-1
blockchain = Blockchain()

## 3- Mining a new Block
### Now we initialize the route decorator 
@app.route('/mine_block', methods=['GET'])
def mine_block():
    ### Here first we need to get the previous block in order to get it's proof
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    
    ### Now we will call the proof of work method as we get the only argument
    ### which it is going to take is previous_proof
    proof = blockchain.proof_of_work(previous_proof)
    
    ### Now once the proof is acquired we need to create this new block and
    ### for that we need two arguments which are proof that we already got and
    ### previous_hash and to get that value we will use the hash method
    previous_hash = blockchain.hash(previous_block)
    
    ### Now let's create this new block and add it to the chain
    block = blockchain.create_block(proof, previous_hash)
    
    ### Now let's create a response to display it in POSTMAN
    response = {'message': 'Congrats, you have just mined a block',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    
    ### Now let's jsonify this response to get it displayed as JSON and it's
    ### response status code will be 200
    return jsonify(response), 200

## 4- Get the full blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    ### Now we just need to get the full chain from the blockchain object
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    
    ### Now let's jsonify this response to get it displayed as JSON and it's
    ### response status code will be 200
    return jsonify(response), 200

## 5- Running the app
    ### In order to run the app it requires two arguments, first is the host
    ### and second is port number, then we select the whole code and execute it
app.run(host = '0.0.0.0', port = 5000)