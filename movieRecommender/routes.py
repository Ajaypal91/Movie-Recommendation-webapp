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


@app.route('/getHomePageData')
def getHomePageData() :
    userID = request.args['userid']
    username = request.args['name']
    if RepresentsInt(userID) :
        status,data = getHomePageDetails(username,userID)
        if status :
            return jsonify(status=True, data=data)
        else :
            return jsonify(status=False, data="No Such User Exists or is Logged In")
    else :
        return jsonify(status=False, data="No Such User Exists or is Logged In")