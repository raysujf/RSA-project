"""
Ledger class for GZFLS_Blockchain Project, store all the Transactions and validate each input Transaction automatically.
"""
from RSA_func import decryptObject
from Transaction_exceptions import *

class Ledger(dict):
    def __init__(self):
        super().__init__(self)
    
    def addTransaction(self, Transaction):
        """
        :param: Transaction - a transaction object that needs to be added into the Ledger
        :return: None

        In this function, you should check whether the input function is valid. If not, raise corresponding exceptions
        as described in part 1.3.1 of project requirement.
        """
        """WRITE YOUR CODE BELOW"""
        if isCoinBase(Transaction):
            self[Transaction.getTxn()]=Transaction
            return
        else:
            self.checkRecursiveTx(Transaction)
            for i in Transaction.inTransaction:
                self[i[0]].outTransaction[i[1]][2]=True
            self[Transaction.getTxn()]=Transaction
        

                
    def checkIsBalance(self, Transaction):
        """
        :param: Transaction - a transaction object that needs to be added into the Ledger
        :return: None

        In this function, you should check whether the input transaction is balance on Input Amount and Output Amount. If
        the transaction is not balanced, raise TransactionNotBalanceError(). If it is balanced, return None
        """
        """ WRITE YOUR CODE BELOW """
        inputAmount=0
        for i in Transaction.inTransaction:
            index=i[0]
            if index not in self:raise TransactionInNotExist()
            inputAmount+=self[index].outTransaction[i[1]][0]
        outputAmount=0
        for i in Transaction.outTransaction:
            outputAmount+=i[0]
        if inputAmount!=outputAmount:
            raise TransactionNotBalanceError()

    
    def checkIsUnused(self, Transaction):
        """
        :param: Transaction - a transaction object that needs to be added into the Ledger
        :return: None

        In this function, you should check whether each entry that .inTransaction points to is unUsed. If any of
        the entry is already used, raise TransactionDoubleSpendError.
        """
        """ WRITE YOUR CODE BELOW """
        for i in Transaction.inTransaction:
            pub=self[i[0]].outTransaction[i[1]][1]
            sig=i[2]
            if decryptObject(sig,pub[0],pub[1])!=hash(self[i[0]]):
                raise TransactionDoubleSpendError()

    def checkInSig(self, Transaction):
        """
        :param: Transaction - a transaction object that needs to be added into the Ledger
        :return: None

        In this function, you should check whether each signature in entry of .inTransaction is valid. If any of
        the signature is invalid, raise TransactionSignatureError.
        """
        """ WRITE YOUR CODE BELOW """
        for in_txn, in_index, signature in Transaction.inTransaction:
            prev_tx = self[in_txn]
            prev_pubKey = prev_tx.outTransaction[in_index][1]
            prev_sig = Transaction.inTransaction[in_index][2]

            sig_result = decryptObject(prev_sig, prev_pubKey[0], prev_pubKey[1])
            if sig_result != hash(prev_tx): raise TransactionSignatureError()
    
    def checkRecursiveTx(self, Transaction):
        """
        :param: Transaction - a transaction object that needs to be added into the Ledger
        :return: None

        In this function, you will check the transaction and their upperstream transactions recursively until you meet
        the transaction from COINBASE. Any transaction from COINBASE is directly considered as valid transaction. If the
        transaction is valid after checking recursively, raise corresponding Exceptions, otherwise, return nothing.
        """
        """ WRITE YOUR CODE BELOW """
        if isCoinBase(Transaction):return
        self.checkIsUnused(Transaction)
        self.checkIsBalance(Transaction)
        self.checkInSig(Transaction)
        for i in Transaction.inTransaction:
            Txn=self[i[0]]
            return self.checkRecursiveTx(Txn)
    
    def getBalanceStat(self):
        """
        :param: Nothing
        :return: A dictionary that represent the total usable (unused) coins in the ledger. The key is the public key of
        receiver while the value is balance (amount of money) under each public key.
        """
        """ WRITE YOUR CODE BELOW """
        tmp = 0
        balance = dict()
        for txn in self.keys():
            for amount, pubkey, isUsed in self[txn].outTransaction:
                if not isUsed:
                    balance.update(pubKey=tmp + amount)
                    tmp = amount
        return balance
            
    

    
    def __str__(self):
        result ="| Status | Current Number of Transaction Stored: {}\n".format(len(self))
        result +="------------ Transactions Stored in Ledger Below ----------\n"
        result +="| Ledger Balence Statistics: " + str(self.getBalanceStat()) + "\n"
        for Txn in self.keys():
            result += str(self[Txn])
            result += "\n|\n"
        result +="------------ Transactions Stored in Ledger Above ----------\n"
        return result
        
    def __repr__(self):
        return str(self)
    
    def exportFile(self, fileName="Ledger.txt"):
        with open(fileName, "w") as exportFile:
            exportFile.write(str(self))

def isCoinBase(transaction):
    return transaction.isCoinBase

def decryptSignature(signature, pubKey: tuple):
    """
    :param: signature - a tuple of tokens formed by encryptObject in RSA_func.py, pubKey - a tuple of integers that contain
    (pubKey, N)
    :return: the decryption result of encrypted message.

    If decryption fail, the normal Exception will be raised instead of the TransactionSignatureError. You can use a
    try:
        ...
    except:
        ...
    structure to 'catch' the exception raised by decryptObject and then raise the TransactionSignatureError instead.
    """
    """ WRITE YOUR CODE HERE """
    return decryptObject(signature,pubKey[0],pubKey[1])

if __name__ == "__main__":
    A = Ledger()
    
