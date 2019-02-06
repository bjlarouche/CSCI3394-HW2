import random
import hashlib
import uuid
import time
import datetime
import json
import math
import matplotlib.pylab as plt
import numpy as np

###########################################
###########################################
## PTR CLASS
###########################################
###########################################

## See (https://stackoverflow.com/a/1145848)
class ptr:
    def __init__(self, obj): self.obj = obj
    def get(self):    return self.obj
    def set(self, obj):      self.obj = obj

###########################################
###########################################
## HELPER FUNCTIONS
###########################################
###########################################

# See (https://www.pythoncentral.io/hashing-strings-with-python)
# If (use_salt : true) then the returned hash will be more random
def hashString(string_to_hash, use_salt):
    # UUID is used to generate a random number
    if (use_salt):
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + string_to_hash.encode()).hexdigest() + ':' + salt
    else:
        return hashlib.sha256(string_to_hash.encode()).hexdigest()

## Generates a nonce w/ default length of 8 if no length is provided
## This is how python-oauth2 does it
## See (https://stackoverflow.com/a/28186447)
def generateNonce(length=8):
    """Generate pseudorandom number."""
    return ''.join([str(random.randint(0, 9)) for i in range(length)])

# Returns a random hexidecimal string
def generateRandomHex():
    randomInt = int(random.random()*100000000) # Random integer 0-100,000,000
    return hex(randomInt).encode('utf-8')

# Returns a random Hash based on a random Hex
def generateRandomHash():
    hexStr = generateRandomHex() # Random hexidecimal string
    return hashlib.sha1(hexStr).hexdigest(), hexStr

# Returns current UTC timestamp in ISO format
def generateTimestamp():
    return datetime.datetime.utcnow().isoformat()

## Plot a line graph
def linePlot(data_array):
    lists = sorted(data_array.items()) # Sorted by key, return a list of tuples

    x, y = zip(*lists) # Unpack a list of pairs into two tuples

    plt.plot(x, y)
    plt.show()

## Plot a box graph with the given labels
def boxPlot(data_array_2d, x_label, y_label):
    fig, ax = plt.subplots()
    pos = np.array(range(len(data_array_2d))) + 1
    bp = ax.boxplot(data_array_2d, sym='k+', positions=pos,
                    notch=1, bootstrap=5000,
                    usermedians=None,
                    conf_intervals=None)
    
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.setp(bp['whiskers'], color='k', linestyle='-')
    plt.setp(bp['fliers'], markersize=3.0)
    plt.show()

###########################################
###########################################
## BLOCK CLASS
## See (https://cryptocurrencyhub.io/implementing-a-simple-proof-of-work-algorithm-for-the-blockchain-bdcd50faac18)
###########################################
###########################################

class Block:
    def __init__(self, index, timestamp, data, previous_hash=''):
        self.index = index,
        self.timestamp = timestamp;
        self.nonce = generateNonce(16);
        self.data = data;
        self.previousHash = previous_hash;
        self.hash = self.calculateHash()
        

    # Calculating the hash value with the nonce property
    def calculateHash(self):
        return hashlib.sha256(json.dumps(self.data).encode() + self.nonce.encode()).hexdigest()

    def mineBlock(self, difficulty):
        # While loop conditional used is a quick trick to make the substring of hash values exactly the lenght of difficulty
        while(self.hash[:difficulty] != "0"*(difficulty)):
            # Incrementing the nonce value everytime the loop runs.
            self.nonce = generateNonce(16);
          
            # Recalculating the hash value
            self.hash = self.calculateHash();
            
        # Logging when a block is created   
        print("Block mined: " + self.hash);

###########################################
###########################################
## BLOCKCHAIN CLASS
## See (https://cryptocurrencyhub.io/implementing-a-simple-proof-of-work-algorithm-for-the-blockchain-bdcd50faac18)
###########################################
###########################################

class Blockchain:
    def __init__(self):
        self.chain = [self.createGenesisBlock()];
  
        # Adding a difficulty property to the Blockchain class
        self.difficulty = 1;
    
    def createGenesisBlock(self):
        return Block(0, generateTimestamp(), "Genesis Block", "0");
    
    def getlatestBlock(self):
        return self.chain[len(self.chain) - 1];
    
    def addBlock(self, newBlock):
        newBlock.previousHash = self.getlatestBlock().hash;
                
        # New method to mine the block
        # Customizable difficulty value
        newBlock.mineBlock( self.difficulty );
  
        self.chain.append(newBlock);
  
    def isChainValid(self):
        i = 1
        while(i < len(self.chain)):
            currentBlock = self.chain[i];
            previousBlock = self.chain[i-1];
            
            if(currentBlock.hash != currentBlock.calculateHash()): # Check for hash calculations
                return False
            
            if(currentBlock.previousHash != previousBlock.hash): # Check whether current block points to the correct previous block
                return False

            i = i + 1

        return True


###########################################
###########################################
## RUN-TIME
###########################################
###########################################

def run():
    myChain = Blockchain();

    # Variables for the while loop
    difficultyTimes = {}
    lastStep = math.floor(time.time())
    timeTaken = 0
    index = 1
    countAtDifficulty = 0
    
    while (timeTaken < 60*5): ## Stop when it takes 5 minutes to mine a block
        lastStep = time.time()
        
        print("Mining block " + str(index) + " at difficulty " + str(myChain.difficulty) + "…");
        myChain.addBlock(Block (index, generateTimestamp(), {"ammount": 20}));

        ## 5 tries at every difficulty
        if (countAtDifficulty >= 4):
            myChain.difficulty = myChain.difficulty + 1
            countAtDifficulty = 0
        else:
             countAtDifficulty = countAtDifficulty + 1
             
        timeTaken = time.time() - lastStep
        # Keep track of how long it takes at wach difficulty level
        if (difficultyTimes.get(str(myChain.difficulty)) != None):
            currentAvg = difficultyTimes[str(myChain.difficulty)]
            difficultyTimes[str(myChain.difficulty)].append(timeTaken)
        else:
            difficultyTimes[str(myChain.difficulty)] = [timeTaken]

        print("It took " + str(timeTaken) + " seconds")
        index = index + 1

    print("Stopping: Time to mine has exceeded 5 minutes.")

    boxData = list(difficultyTimes.values()) # Make dict a list (flatten)
    boxPlot(boxData, 'Difficulty', 'Time (Seconds)')

run()

