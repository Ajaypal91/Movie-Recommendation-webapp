import pandas as pd
import numpy as np
import os
import movieRecommender.DAO.userDAO as UD
reload(UD)

class User(object) :
    def __init__(self, user=None,passwd=None) :
        self.name = None
        self.user = user
        self.userHist = None
        self.userID = None
        self.passwd = passwd

    def getUserID(self):
        return self.userID

    def getUsrHist(self):
        return self.userHist

    def usrLogin(self,userName,passw) :

        userID = UD.authenticateUser(userName.lower(),passw)
        if userID != None :
            self.user = userName
            self.name = userName.upper()
            self.userID = userID
            # self.userHist = UD.getUserHistory(userID)
            # if len(self.userHist) == 0 : #no user history found
            #     return -1
        # if userName.lower().strip() == "ajay":
        #     if passw.strip() == "11":
        #         self.user = userName
        #         self.name = userName.upper()
        #         self._loadUserProfile()
            return True
        else:
            return False
        # else:
        #     return False

    def _loadUserProfile(self) :
        path = os.getcwd() + "/movieRecommender/Data/Histories/%s_hist.csv" %self.name.lower()
        self.userHist = pd.read_csv(path,names=["MovieID","LD"]).as_matrix()
        #print self.userHist

    def isUserLogedIn(self):
        return UD.isUserActive(self.userID)

    def createNewUser(self):
        return UD.createNewUser(self.user,self.passwd)

class UserProfile(User) :
    
    def __init__(self,user) :
        super(UserProfile,self).__init__()
        self.name = user.name
        #self.userHist = user.userHist
        self.profile = None
    
    def getUserProfile(self) :
        return self.profile
    
    def createUserProfile(self,userID,Xcorpus,userHist,userHistoryUpdated=0) :
        create = 0
        #check if user history is updated? If yes, then create user profile again
        if userHistoryUpdated == 0 : #not updated
            status,data = UD.loadUserProfile(userID)
            if not status : #could not load profile then create one or profile does not exist so create one
                create = 1
            else : #successful in fetching userprofile
                self.profile = data #set profile and return
                return

        #else create new profile
        @np.vectorize
        def selected(elem) : return elem in userHist[:,0]
        XforUsers = Xcorpus[selected(Xcorpus[:,0])]
        #print XforUsers
        userProfile = userHist[:,1].T.dot(XforUsers[:,1:])
        self.profile = userProfile
        UD.updateUserProfile(userID,self.profile)

        
        
