from flask import Flask, render_template, request, redirect, url_for, session
import hashlib
import csv
import os

app = Flask(__name__)
data = dict()
app.secret_key = os.urandom(32)

def checkSession():
    if 'usr' in session:
        return render_template("common.html",t="Logged In",mes="You are successfully logged in as"+session['usr'],p="/logout",m='GET',b="LogOut")
    return render_template("login.html")

@app.route("/")
def home():
    readFile()
    return checkSession()

@app.route("/register", methods=['POST'])
def register():
    usr = request.form["usr"]
    pw = request.form["pw"]
    if usr == "" or pw == "":
        return render_template("common.html",t="registration failure",mes="Please Fill out all information.",p="/registerNew",m='POST',b="Back")
    elif usr in data:
        return render_template("common.html",t="registration failure",mes="Username already exist",p="/",m='POST',b="Login")
    else:
        hashObj = hashlib.sha1()
        hashObj.update(pw)
        postPw = hashObj.hexdigest()
        writeFile(usr,postPw)
        readFile()
        return render_template("common.html",t="Register Success",mes="Registered successfully!",p="/",m='GET',b="Login")

@app.route("/registerNew", methods=['POST'])
def registerPage():
    return render_template("register.html")


@app.route("/auth", methods=['POST'])
def loginCheck():
    hashObj = hashlib.sha1()
    usr = request.form["usr"]
    hashObj.update(request.form["pw"])
    pw = hashObj.hexdigest()
    if usr in data:
        if data[usr] == pw:
            session['usr'] = usr
            return render_template("common.html",t="Success",mes="Successfully logged in!",p="/logout",m='GET',b="LogOut")
        else:
            return render_template("common.html",t="Failed",mes="Incorrect Password!",p="/",m='GET',b="Back")
    else:
        return render_template("common.html",t="Failed",mes="Username Doesn't Exist",p="/",m='GET',b="Back")

@app.route("/logout")
def logout():
    session.pop('usr')
    return render_template("common.html",t="Log Out",mes="You have successfully logged out!",p="/",m='GET',b="Login")

def readFile():
    with open('data.csv','r') as csvfile:
        dataReader = csv.reader(csvfile)
        for row in dataReader:
            if row[0] != "Usr" and row[1] != "Pw" and (row[0] not in data) :
                data[row[0]] = row[1]

def writeFile(u,p):
    with open('data.csv','w') as csvfile:
        dataWriter = csv.writer(csvfile)
        dataWriter.writerow([u,p])

if __name__ == "__main__":
    app.debug = True
    app.run()

