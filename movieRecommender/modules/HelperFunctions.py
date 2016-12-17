import pandas as pd
import numpy as np
import os
import random
import re
from sklearn import preprocessing

#this is a class of helper functions which process the raw data
class RawDataProcessing(object) :
    
    def __init__(self,path,namesCol) :
        #this will be used for searching
        self.d1 = pd.read_csv(path,names=(namesCol))
        
    @staticmethod    
    def getGenersList() :
        return ["Action","Adventure","Animation","Children","Comedy","Crime","Documentary","Drama","Fantasy","Film-Noir","Horror","Musical","Mystery","Romance","Sci-Fi","Thriller","War", "Western"]
        
    def applyMapFunction(self,funcToApply,fromCol,toCol) :
        self.d1[toCol] = 0
        self.d1[toCol] = self.d1[fromCol].map(funcToApply)
    
    def createGenerFeatures(self,genersList) :
        i = 0
        def createGeners(x) :
            if genersList[i] in str(x) :
                return 1
            else :
                return 0
        while i < len(genersList) :
            self.d1[genersList[i]] = 0
            self.d1[genersList[i]] = self.d1.gener.map(createGeners)
            i += 1
    
    def printSample(self,rowsToPrint) :
        print self.d1.head(rowsToPrint)
    
    def extractFeaturesWithIds(self,cols) :
        self.d1 = self.d1.drop(self.d1.columns[cols],axis=1)  
            
    def getNumpyX(self) :
        #return the numpy array removing the id column
        #return self.d1.drop(self.d1.columns[0],axis=1).as_matrix()
        return self.d1.as_matrix()
        
    def createDF(self,cols) :
        dfList =  [len(self.d1[self.d1[self.d1.columns[x]] == 1]) for x in cols]
        return dfList 
        
#this is class to prepare IDF's and Xcorpus of feature arrays
class createDataFramesAndIntialFeatureArray(object) :
    
    def __init__(self) :
        self.idAndMovie = None
        self.IDF = None
        self.Xcorpus = None
        self.processingDataObj = None
    
    def updateXcorpus(self,val) :
        self.Xcorpus = val
            
    def getXcorpus(self):
        return self.Xcorpus
        
    def getIDF(self):
        return self.IDF
           
    def getFilePath(self,filename) :
        return os.getcwd() + "/movieRecommender/Data/" + filename
    
    def getRawData(self,path) :
        names = ["ID","name","gener","UR","ML"]
        self.processingDataObj = RawDataProcessing(path,names)

    def createCriticsReview(self) :
        #create critics rating randomly from 0 to 5
        crRFun = lambda x : random.randint(1,5)
        self.processingDataObj.applyMapFunction(crRFun,"CR","CR")
        #self.processingDataObj.printSample(5)
    
    def createYearMovieReleased(self) :        
        pattern = "\([0-9]*\)"
        def findMovieYear(x) :
            if x != None:
                year = re.search(pattern,x).group(0).replace("(","").replace(")","")
                return year
        self.processingDataObj.applyMapFunction(findMovieYear,"name","MY")
        #self.processingDataObj.printSample(4) 
                                               
    def createGeners(self) :
        genersList = RawDataProcessing.getGenersList()
        self.processingDataObj.createGenerFeatures(genersList)
        #self.processingDataObj.printSample(7)
     
    def createIDF(self,dfListCorpus) :
        numSampCorpus = len(self.processingDataObj.d1)
        idfListCorpus = [np.log10(numSampCorpus/x) for x in dfListCorpus]
        #self.IDF  = preprocessing.MinMaxScaler().fit_transform(np.concatenate((np.array([0.5,0.5,0.5,0.5]), idfListCorpus),axis=0)) 
        self.IDF  = np.concatenate((np.array([0.5,0.5,0.5,0.5]), idfListCorpus),axis=0)
        #print self.IDF
            
    def processData(self,pathToFile) :
        ##fetch the file
        self.getRawData(pathToFile)
        
        #################################################
        ### CREATING CRITICS REVIEW FEATURE RANDOMLY ####
        #################################################
        self.createCriticsReview()
        
        #################################################
        ### CREATING Year realeased movie feature ####
        #################################################
        self.createYearMovieReleased()
             
        #################################################
        ###         CREATING geners feature          ####
        #################################################
        self.createGeners()
        
        #extract first to columns to idMovie column
        self.idAndMovie = (self.processingDataObj.d1[self.processingDataObj.d1.columns[[0,1]]]).as_matrix()
        
        #################################################
        ###         Time to normalize things         ####
        #################################################
        #extract only the features columns
        deleteCols = [1,2]
        self.processingDataObj.extractFeaturesWithIds(deleteCols)
        #self.processingDataObj.printSample(4)
        
        #################################################
        ###             Extract DataSet              ####
        #################################################
        dataSet = self.processingDataObj.getNumpyX()
        #print dataSet[1]
        #######################################################
        ### Normalize DataSet to range 0-1 for each feature####
        #######################################################
        min_max_scaler = preprocessing.MinMaxScaler()
        X_train_minmax = min_max_scaler.fit_transform(dataSet[:,1:])
        #print X_train_minmax[0]
        
        self.Xcorpus = np.concatenate((dataSet[:,0].reshape(len(dataSet),1),X_train_minmax),axis=1)
        #print self.Xcorpus[0]      
        
        #Append id column to the X_train_minmax normalized values
        #X_train_minmax = np.concatenate(self.processingDataObj.d1[self.processingDataObj.d1.columns[0]].as_matrix().T,X_train_minmax)
        
        #######################################################
        ### create Document frequency for geners features####
        #######################################################
        colsListGeners = range(5,23)
        dfListCorpus = self.processingDataObj.createDF(colsListGeners)            
        #print dfListCorpus
        
        ############################################################
        ### create InverseDocument frequency for geners features####
        ############################################################
        self.createIDF(dfListCorpus) 
        
               
'''
#create the dataframes and fetaure datasets required     
createDataObject = createDataFramesAndIntialFeatureArray()
#initial filepath               
filename = "MoviesLength.csv"                  
pathToFile = createDataObject.getFilePath(filename)
createDataObject.processData(pathToFile)
'''