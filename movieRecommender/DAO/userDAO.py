import  movieRecommender.DAO as DB
import pandas as pd
import cPickle as pickle
import json
import movieRecommender.DAO.engineDAO as ED

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
    status = db.query_formatted('update user_data set historyupdated=1 where id=%s', [userID])
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
    profile = pickle.dumps(profile)
    # quer = "update user_data set userprofile=%s where id=%s" % (profile,userID)
    # status = db.query(quer)
    db.update('user_data',row={'id':userID},userprofile=profile)
    status = db.query_formatted('update user_data set historyupdated=0 where id=%s', [userID])
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

def getHistoryForUser(userid,batchno) :
    hist = getUserHistory(userid,histFormat='json')

    #if no history is present
    if len(hist) == 0 :
        return -1,hist,0 #return status = -1, data as hist, and 0 as number of batches

    decoder = json.JSONDecoder()
    hist_json = decoder.decode(hist)

    #get list of movies from user history
    idsList = []
    for x in hist_json :
        idsList.append(int(x['id']))

    #get list of movies
    moviesList = ED.getMoviesFromIDs(idsList)

    #create final data list of dictonaries/json
    final_data = []
    for x, y in zip(hist_json, moviesList):
        final_data.append({'id': x['id'], 'name': y['name'], 'liking': x['liking']})


    batches = len(final_data) / 10  if  (len(final_data)%10 == 0)  else  len(final_data) / 10 + 1
    batchno = int(batchno)
    if batches >= int(batchno) :
        return True,final_data[(batchno-1)*10:batchno*10],batches #return status, that batch of history and number of batches


def updateHistory(userID, movieID,liking):
    hist = getUserHistory(userID, histFormat='json')


    histData = {}
    histData["id"] = movieID
    histData["liking"] = liking

    status = False

    #if history is empty
    if len(hist) == 0 :
        updatedHist = []
        updatedHist.append(histData)
        encoder = json.JSONEncoder()
        updatedHist = encoder.encode(updatedHist)
        #update the tables
        status = updateUserHistory(userID,updatedHist)
    else :
        decoder = json.JSONDecoder()
        hist_json = decoder.decode(hist)
        movieIDPresent = False
        #check if movie id is already present and liking is same
        for x in hist_json :
            if x['id'] == movieID :
                if x['liking'] != liking :
                    x['liking'] = liking
                    movieIDPresent = -1
                else :
                    movieIDPresent = True
        status = True
        #if not present add the entry
        if not movieIDPresent :
            hist_json.append(histData)
            encoder = json.JSONEncoder()
            updatedHist = encoder.encode(hist_json)
            status = updateUserHistory(userID, updatedHist)

        if movieIDPresent == -1 :
            encoder = json.JSONEncoder()
            updatedHist = encoder.encode(hist_json)
            status = updateUserHistory(userID, updatedHist)

    return status


