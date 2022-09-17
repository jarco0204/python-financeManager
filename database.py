import sqlite3
from sqlite3 import Error


#Pre-define statements to create entities
createTransactionAggregate= "CREATE TABLE IF NOT EXISTS MoneyTransaction(id INTEGER PRIMARY KEY NOT NULL,date TEXT NOT NULL,moneyValue REAL NOT NULL, reasonTransaction TEXT NOT NULL, transactionCategory TEXT, Vendor TEXT, FOREIGN KEY (id) REFERENCES BankAccount (id));"
createBankAccountAggregate= "CREATE TABLE IF NOT EXISTS BankAccount( id INTEGER PRIMARY KEY, balance REAL NOT NULL);"

#Pre-define statements to add information to entities
addBankTran= "INSERT INTO BankAccount(id,balance) values(?,?);"
addTransaction= "INSERT INTO MoneyTransaction(id,date,moneyValue,reasonTransaction,transactionCategory,vendor) VALUES(?,?,?,?,?,?);"

#Pre-define statements to ammend inserted data
updateBankTran= "UPDATE BankAccount SET balance=? WHERE id=?;"


#------------------------------ Database functions----------------------------------------
def createConnection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn #  returns a Connection object which represents an SQLite databas
    except Error as e:
        print(e)

def createTable(conn, sqlStatement):
    """ create a table from the sqlStatement
    @param conn: Connection object
    @param sqlStatement: a CREATE TABLE statement
    """
    try:
        c = conn.cursor()
        c.execute(sqlStatement)
    except Error as e:
        print(e)

def executeADDSQL(conn,sqlStatement,entry):
    cur= conn.cursor()
    cur.execute(sqlStatement,entry)
    return cur.lastrowid

# This function needs to be modified because there might several things that one might want to update, or maybe just one thing
def updateTransaction(conn,task):
    updateTransaction= "UPDATE MoneyTransaction SET vendor=? WHERE id=?;" #ONLY updates date
    cur= conn.cursor()
    cur.execute(updateTransaction,task)
    conn.commit()

def retrieveBankBalance(conn,id):
    cur= conn.cursor()
    cur.execute("SELECT balance From BankAccount WHERE id=?",(id,)) #We write a comma after id because it is a tuple
    return cur.fetchall()

def retrieveMoneyTransaction(conn,id):
    cur= conn.cursor()
    cur.execute("SELECT * From MoneyTransaction WHERE id=?",(id,)) #We write a comma after id because it is a tuple
    return cur.fetchall()


