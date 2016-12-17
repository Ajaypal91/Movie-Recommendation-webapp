from flask import Flask, redirect, url_for, render_template,request, jsonify
import json
from movieRecommender import app
from movieRecommender.modules import *


# home page render template
@app.route('/login')
def login():
    argsLen = request.args.__len__()
    if argsLen > 0:
        if 'showInvalidStatus' in request.args :
            showInvalidStatus = request.args['showInvalidStatus']
            if showInvalidStatus == "show" :
                return render_template('main.html', showInvalidStatus=showInvalidStatus)
            else :
                return render_template('main.html', showInvalidStatus="hide")
    else :
        return render_template('main.html', showInvalidStatus="hide")


# Login called method
@app.route('/authenticateUser', methods = ['POST'])
def authenticateUser():
    # threshold defined for candidate selection
    threshold = 0.7
    # check user name and password
    user = request.form['username']
    password = request.form['password']
    status,userName,userID = checkAuthentication(user,password)

    if status :
        return redirect(url_for('home', name = userName,userid=userID))
    else :
        return redirect(url_for('login',showInvalidStatus="show"))

#404 page loader
@app.errorhandler(404)
def page_not_found(error):
    return render_template('InvalidPage.html'), 404

#load home page for user
@app.route('/home/<name>/<userid>')
def home(name,userid) :
    return render_template('home.html',name=name,userid=userid)

#route to load data for home page
@app.route('/getHomePageData')
def getHomePageData() :
    userID = request.args['userid']
    username = request.args['name']
    if RepresentsInt(userID) :
        status,data = getHomePageDetails(username,userID)
        #if no history found for user
        if status == -1 :
            helpText = 'No movies history found. <br/> Please Click on Build/Update History to create one.'
            return jsonify(status=status,data=helpText)
        #if everything went fine
        if status :
            return jsonify(status=True, data=data)
        else :
            return jsonify(status=False, data="No Such User Exists or Logged In")
    else :
        return jsonify(status=False, data="No Such User Exists or Logged In")

@app.route('/signup',methods=['GET'])
def signup() :
    return render_template('signup.html')

@app.route('/createnewuser',  methods = ['POST'])
def createnewuser():
    user = request.form['username']
    password = request.form['password']
    status = createUser(user,password)
    if status :
        return redirect(url_for('login'))
    else : #show error message
        pass

#signout route
@app.route('/logout',methods=['GET'])
def logout() :
    url = request.url;
    userID = url.replace('http://localhost:5000/logout?','').replace('=','')
    userLogout(userID)
    return redirect(url_for('login'))

#history route
@app.route('/history',methods=['GET'])
def getHistory() :
    userID = request.args['userid']
    batchno = request.args['batchno']
    status,data,batches = getHistoryForUser(userID,batchno)
    # if no history found for user
    if status == -1:
        helpText = 'No movies history found. <br/> Please Click on Build/Update History to create one.'
        return jsonify(status=status, data=helpText,nobatches=batches)
    else :
        return jsonify(status=status, data=data, nobatches=batches)


#search api
@app.route('/search',methods=['GET'])
def search():
    searchText = request.args['searchtext']
    batchno = request.args['batchno']
    status, data, batches = getSearchResults(searchText, batchno)
    if not status :
        errorMsg = 'No result found'
        return jsonify(status=-1,data=errorMsg,nobatches=0)
    else :
        return jsonify(status=status, data=data, nobatches=batches)

#updatehistory for the user
@app.route('/updatehistory',methods=['GET'])
def updatehistory():
    userid = request.args['userid']
    movieid = request.args['movieid']
    liking = request.args['liking']
    status = updatehistoryForUser(userid,movieid,liking)

    if status :
        return jsonify(status=status)
    else :
        errMsg = 'Something went wrong. Could not update the history'
        return jsonify(status=status,data=errMsg)
