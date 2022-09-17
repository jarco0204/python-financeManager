#libraries
import database as dataBase

#GLOBAL Variables
firstTime= False
id = 27# first transaction was 24
pos = {1:"Purchase",2:"Withdrawal",3:"Payroll"}
categories= {1:"Personal Care",2:"Renumeration",3:"Transportation",4:"Groceries",5:"Entertainment", 6:"Work",7:"Payment"}

def main():
    id= readId()
    sqlDB= dataBase.createConnection("financeDB.db") #Establishing connection with the Database
    if sqlDB is None:
        print("Database connection could not be established")
    if(firstTime):
        bankBalance= float(input("Enter your bank account: "))
        dataBase.createTable(sqlDB,dataBase.createBankAccountAggregate)
        dataBase.createTable(sqlDB,dataBase.createTransactionAggregate)
        #User must enter the last transaction in order to save current bank balance
        dateTran= input("When was your last purchase: ")
        valueTran= float(input("What is the value of this transaction: "))
        reason= pos[input("What is the reason for transaction? (1:Purchase,2:Withdrawal,3:Payrol)" )]
        print("Options are: 1:Purchase, 2:Renumeration,3:Transportation,4:Groceries, 5:Entertainment")
        categoryTran= categories[input("In which category this transaction falls?: ")]
        #------ Values have been read, add to database---
        with sqlDB:
            bankAccountEntry= (id,bankBalance)
            dataBase.executeADDSQL(sqlDB,dataBase.addBankTran,bankAccountEntry)
            moneyTransaction= (id,dateTran,valueTran,reason,categoryTran)
            dataBase.executeADDSQL(sqlDB,dataBase.addTransaction,moneyTransaction)
    else:
        while(True):
            print("Welcome master Johan!")
            decision= int(input("What job are you looking to complete?: (1:Update, 2:Add Transaction 3: Visualize) "))
            if(decision == 1):
                jobToUpdate= input("Do you want to update a Bank Transaction or Money Transaction?: (1:Bank, 2:Money)")
                transactionNum= int(input("Enter transaction Id: "))
                with sqlDB:
                    if(jobToUpdate=="1"):
                        sqlToUse= dataBase.updateBankTran
                        newBalance=input("Enter new balance to update: ")
                        dataBase.updateTransaction(sqlDB,(newBalance,transactionNum))
                    else:
                        # print("Options are: 1:Personal Care, 2:Renumeration,3:Transportation,4:Groceries, 5:Entertainment")
                        # newCategory=categories[int(input("In which category this transaction falls?: "))]
                        vendor= str(input("Where was this transaction carried out: "))
                        print(vendor)
                        # # update= newCategory +","+vendor
                        # dataBase.updateTransaction(sqlDB,(newCategory,transactionNum))
                        #newDate= input("Enter new date to update: (format d-m-y)")
                        # print(type(newDate))
                        dataBase.updateTransaction(sqlDB,(vendor,transactionNum))
                
                    
            elif(decision==2):
                dateTran= input("Enter the date of this transaction: (d-m-y)  ")
                valueTran= float(input("What is the value of this transaction: "))
                reason= pos[int(input("What is the reason for transaction? (1:Purchase,2:Withdrawal,3:Payrol)" ))]
                if(reason=="Purchase" or reason=="Withdrawal"):
                    valueTran=-valueTran # making it negative
                print("Options are: 1:Personal Care, 2:Renumeration,3:Transportation,4:Groceries, 5:Entertainment, 6:Work, 7:Payment")
                categoryTran= categories[int(input("In which category this transaction falls?: "))]
                vendor= input("Who is the vendor? ")
                with sqlDB:
                    bankBalance= findLatestBalance(sqlDB,id)+valueTran #based on last id
                    id+=1 #Updating Id to save in Database
                    bankAccountEntry= (id,bankBalance)
                    dataBase.executeADDSQL(sqlDB,dataBase.addBankTran,bankAccountEntry)
                    moneyTransaction= (id,dateTran,valueTran,reason,categoryTran,vendor)
                    dataBase.executeADDSQL(sqlDB,dataBase.addTransaction,moneyTransaction)
                    writeId(id) #Update the ID of Transaction

                
            elif(decision==3):
                decisionVi= int(input("Do you want to visualize a particular  Money transaction (1), bank account (2)"))
                idTra= int(input("Enter the transaction id: "))
                with sqlDB:
                    if (decisionVi == 1):
                        print(dataBase.retrieveMoneyTransaction(sqlDB,idTra))
                    else:
                        print(dataBase.retrieveBankBalance(sqlDB,idTra))



            else:
                print("Wrong input, try again next time ;)")
            quit= int(input("Do you want to complete another operation? (1:Yes, 2:No)"))
            if(quit==2):
                break


    sqlDB.close() #closing resources

def findLatestBalance(connec, id):
    bankBal=dataBase.retrieveBankBalance(connec, id)  
    return bankBal[0][0] #returning first value of tuple as float
def readId():
    """Designed to read the Id that it is saved in a text file"""
    file= open("idBank.txt","r")
    id= int(file.readline())
    file.close()
    return id

def writeId(idWrite):
    """Designed to update the last id after a transaction"""
    file=open("idBank.txt","w") #Erase all of its contents
    file.write(str(idWrite))
    file.close()
main()
