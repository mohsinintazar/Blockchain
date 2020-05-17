# Module 1 - Create a Blockchain
# To be installed:
# Flask: pip install Flask
# Postman: Http Client

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
            if hash_operation[:4] == '00000':
                check_proof = True
            else:
                new_proof += 1
        
        ### Now once we get the puzzle solved we return this new_proof, so it
        ### can be returned to the create_block method
        return new_proof
    
    
# Part-2 - Mining our Blockchain