from pg import DB

#get db connection
def getDBConnection():
    return DB(dbname='mydb', host='localhost', port=5432, user='ajay', passwd='1111')
