"""
This is a version of transaction written by mark
"""
from RSA_func import *
from random import random
from Ledger import Ledger
import time

class Transaction:
    def __init__(self, allTransaction: Ledger, amount: int, myPubKey: tuple, myPrivateKey: tuple, receiverPubKey: tuple, isCoinBase=False):
        """
        :params:
        allTransaction - the ledger that store all valid transactions
        amount - the amount of coin you want to transact to others
        myPubKey - a tuple (myPublicKey, myN)
        myPrivateKey - a tuple (myPrivateKey, myN)
        receiverPubKey - a tuple (receiverPublicKey, receiverN)

        :returns: None

        Create a new transaction object that has appropriate .inTransaction and .outTransaction proprties.
        If the transaction is from COINBASE, the .inTransaction can be empty.

        Structure of Transaction Object
        =================================================================================
        |   isCoinBase  |       inTransaction         |       outTransaction            |
        |---------------+-----------------------------+---------------------------------|
        |               |  Txn  |  index  | Signature | Amount | ReciverPubKey | isUsed |
        |               |-------+---------+-----------+--------+---------------+--------|
        |     False     |1233456|    0    | (tokens)  |   50   |  (pubKey, n)  | False  |
        |               |1233457|    2    | (tokens)  |   50   |  (pubKey, n)  | False  |
        |               |1233458|    0    | (tokens)  |        |               |        |
        =================================================================================
        One tuple in the self.inTransaction represents a tuple in a specific Transaction object's
        .outTransaction property.
        """
        #### Properties that is used to form Unique ID (Txn) for one Transaction Object ###
        # DO NOT MODIFY THESE PROPERTIES
        self.tx_time = int(time.time() * 10000)
        self.randID = int(random() * 10000)
        ###################################################################################

        ############# The Important Properties of a Transaction Object ####################
        self.isCoinBase = isCoinBase
        self.inTransaction = []
        self.outTransaction = []
        ###################################################################################
        """ WRITE YOUR CODE BELOW """
        self.amount=amount
        self.PubKey=myPubKey
        self.PrivateKey=myPrivateKey

        count = 0
        if not self.isCoinBase:
            arr = getMyTransaction(allTransaction, myPubKey)
            for txn, index in arr:
                count += allTransaction[txn].outTransaction[index][0]
                self.addInputTransaction(txn, index, signSignature(allTransaction[txn], myPrivateKey))
                if count == amount:
                    self.addOutputTransaction(amount, receiverPubKey)
                    break
                elif count > amount:
                    self.addOutputTransaction(amount, receiverPubKey)
                    self.addOutputTransaction(count - amount, myPubKey)
                    break
        else:
            self.addOutputTransaction(amount, receiverPubKey)
        print(self.inTransaction, self.outTransaction)



    def addInputTransaction(self, txn, index, Signature):
        """
        You can use this function to add an entry into the Transaction Object's inTransaction property
        """
        """ WRITE YOUR CODE BELOW """
        self.inTransaction.append((txn,index,Signature))
    
    def addOutputTransaction(self, amount, reciverPubKey):
        """
        You can use this function to add an entry into the Transaction Object's outTransaction property
        """
        """ WRITE YOUR CODE BELOW """
        self.outTransaction.append((amount,reciverPubKey,False))
    
    def getTxn(self):
        """
        Return a positive integer that represents the Unique Transaction ID (Txn) of current Transaction.
        """
        return hash(self)

    ############ You Needn't Read & SHOULD NOT Modify the Functions in this class Below #############

    def __hash__(self):
        return abs(hash(self.tx_time) + hash(tuple(self.inTransaction)) + self.randID)
    
    def __str__(self):
        result = "============ Transaction ===============\n"\
        "| Txn: {} \n".format(self.getTxn())
        if self.isCoinBase:
            result += "| THIS TRANSACTION IS FROM COINBASE \n"
        else:
            result += "| In Transactions:\n"\
            "| Txn | Index | Signature |\n"
            for inTx in self.inTransaction:
                result += "| {} | {} | {}\n".format(inTx[0], inTx[1], inTx[2])
        result += "| Out Transactions:\n"\
            "| Amount | reciver PubKey | isUsed\n"
        for outTx in self.outTransaction:
            result += "| {} | {} | {}\n".format(outTx[0], outTx[1], outTx[2])
        result += "========================================"
        return result
    
    def __repr__(self):
        return str(self)
    
    #################################################################################################


# Auxilary Function that used to create a transaction
def getMyTransaction(allTransaction, pubKey):
    """
    :params:
    allTransaction - a Ledger object that store all the accepted valid transactions
    pubKey - the publicKey of receiver.
    :returns:
    A list of Transaction ID and Index that points to a specific entry in the .outTransactions of
    one transaction in Ledger.
    """
    """ WRITE YOUR CODE BELOW """
    MyTransactions = []
    for Txn in allTransaction:
        for index in range(len(allTransaction[Txn].outTransaction)):
            outTx = allTransaction[Txn].outTransaction[index]
            if outTx[1] == pubKey and (not outTx[2]):
                MyTransactions.append((Txn, index))
    return MyTransactions
    

def signSignature(transaction, privateKey: tuple):
    """
    Sign the signature on given Transaction, the privateKey is a tuple (privateKey: int, N: int)
    :params:
    transaction - a Transaction Object
    privateKey - a tuple of (PrivateKey, N)
    :returns:
    Signature of **hash of input transaction** with the given private key.
    """
    """ WRITE YOUR CODE BELOW """
    return encryptObject(hash(transaction), privateKey[0], privateKey[1])

