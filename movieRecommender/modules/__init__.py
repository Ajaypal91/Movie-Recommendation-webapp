import createData as CD
import Users as US
import pickle
import os
from ast import literal_eval    
import json
import pandas as pd
import movieRecommender.DAO.userDAO as UD
import movieRecommender.DAO.engineDAO as ED

reload(ED)
reload(UD)
reload(CD)
reload(US)

#threshold defined for candidate selection 
threshold = 0.7
myUser = None
startCreation = None

def checkAuthentication(user,password) :
    #authenticate User
    myUser = US.User()
    val = myUser.usrLogin(user,password)
    #if valid user saveUser and Load/create relevant data
    if val :
        #save user
        # saveUser(myUser)
        #load/create data based on if history has been changed or not
        # obj = loadData(myUser)
        # global startCreation
        # startCreation = obj
        #return and display top 10 predictions for him
        # result = createJsonData(startCreation.top10Pred)
        # return jsonify(status=True,data=result,name=startCreation.usr.name)
        return True, myUser.name,myUser.userID
    else :
        return False,myUser.name,None



def loadData(myUser):
    #first check if history is updated or not
    threshold = 0.6
    # 1 means updated 0 means not
    isUpdated = UD.isUserHistoryUpdated(myUser.userID)
    obj = CD.createDatasetsForUser(myUser)
    #the following function creates new user profile if history is updated
    obj.start(threshold,isUpdated)
    return obj

#method to load userDetails from its name (change it to ID in future)
def _loadUserFromID(myUser) :
    isUserLoggedIn = myUser.isUserLogedIn()
    return bool(isUserLoggedIn)

# #method to retrieve details for home page
def getHomePageDetails(name,userID) :
    #create User Object
    myUser = US.User()
    #update its id
    myUser.userID = userID
    myUser.user = name.lower()
    #if user is active load its details
    if _loadUserFromID(myUser) :
        obj = loadData(myUser)
        data = ED.getMoviesFromIDs(obj.top10PredIDs)
        # global startCreation
        # startCreation = obj
        # # return and display top 10 predictions for him
        # result = createJsonData(startCreation.top10Pred)
        return True,data
    else :
        return False,None

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
