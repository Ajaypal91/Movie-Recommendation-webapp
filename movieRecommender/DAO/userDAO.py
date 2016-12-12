import  movieRecommender.DAO as DB
import pandas as pd
import cPickle as pickle

#get User history
def getUserHistory(userId,histFormat='dataframe') :
    #get database connection
    db = DB.getDBConnection()
    quer = 'select history from user_data where id=%s' %str(userId)
    hist = db.query(quer)
    if len(hist.getresult()) > 0:
        hist_json = hist.dictresult()[0]['history']

        #no history was created yet
        if len(hist_json) == 0 :
            return hist_json

        if histFormat == 'json' :
            return hist_json
        else :
            return pd.read_json(hist_json, orient='records')
    else : #if no history is present
        return ''

def authenticateUser(userName,password) :
    db = DB.getDBConnection()
    result = db.query_formatted('select id from users where username=%s AND password=%s', (userName, password))
    if len(result.getresult()) > 0 :
        userID = result.getresult()[0][0]
        status = _updateIsActive(userID)
        if status :
            return userID
        else :
            #throw error here in future and show message in UI that user does not exits
            return None
    else :
        # throw error here in future and show message in UI that user does not exits
        return None

def _updateIsActive(userID) :
    db = DB.getDBConnection()
    status = db.query_formatted('update users set isactive=1 where id=%s', [userID])
    return status

def isUserActive(userID) :
    db = DB.getDBConnection()
    result = db.query_formatted('select id from users where id=%s AND isactive=%s', [userID,'1'])
    isActive = 0
    if len(result.getresult()) > 0:
        isActive = result.getresult()[0][0]
    return isActive

def isUserHistoryUpdated(userID) :
    db = DB.getDBConnection()
    result = db.query_formatted('select historyupdated from user_data where id=%s', [userID])
    if len(result.getresult()) > 0:
        return result.getresult()[0][0]
    #if could not find the result just send that history is updated so that the data can be recreated
    return 1

#fucntion not used yet
def updateUserHistory(userID,hist=None):
    db = DB.getDBConnection()
    status = db.query_formatted('update user_data set historyupdated=0 where id=%s', [userID])
    if status : #update was successful
        #update history if exists
        if hist != None :
            status = db.query_formatted('update user_data set history=%s where id=%s', [hist,userID])
            if status : #update was successful
                return True
            else :
                return False
        else :
            return True
    else :
        return False

def loadUserProfile(userID) :
    db = DB.getDBConnection()
    result = db.query_formatted('select userprofile from user_data where id=%s', [userID])
    if len(result.getresult()) > 0:
        dataString =  result.getresult()[0][0]
        #if userprofile exists
        if len(dataString) > 0 :
            return True,pickle.loads(dataString)
        else : #create new userprofile
            return False,dataString
    # if could not find the userprofile handle exception
    return False,None

def updateUserProfile(userID,profile) :
    db = DB.getDBConnection()
    status = db.query_formatted('update user_data set userprofile=%s where id=%s', [profile,userID])
    return status

def createNewUser(username,passwrd) :
    db = DB.getDBConnection()
    #create entry in users table
    status = db.query_formatted('insert into users(username,password,isactive) values(%s,%s,%s)',[username.lower(),passwrd,'0'])
    status = bool(status)

    #now update the user_data table
    if status :
        #get userid
        result = db.query_formatted('select id from users where username=%s AND password=%s AND isactive=%s', [username.lower(),passwrd,'0'])
        if len(result.getresult()) > 0:
            userID = result.getresult()[0][0]
            #create entry in userdata table with default values
            status = db.query_formatted('insert into user_data(id,history,historyupdated,userprofile) values(%s,%s,%s,%s)',[userID, '', '0',''])
            return bool(status)
        else :
            return False

    return status

#method to logout the user
def disableActive(userID) :
    db = DB.getDBConnection()
    status = db.query_formatted('update users set isactive=%s where id=%s', ['0', userID])
    return status


