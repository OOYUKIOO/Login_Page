from flask import Flask, render_template, request, redirect, url_for
import hashlib
import csv

app = Flask(__name__)
data = dict()

@app.route("/")
def home():
    readFile()
    return render_template("login.html")

@app.route("/register", methods=['POST'])
def register():
    usr = request.form["usr"]
    pw = request.form["pw"]
    if usr == "" or pw == "":
        return render_template("common.html",t="registration failure",mes="Please Fill out all information.",p="/registerNew",b="Return to Register")
    elif usr in data:
        return render_template("common.html",t="registration failure",mes="Username already exist",p="/",b="Return to Login")
    else:
        hashObj = hashlib.sha1()
        hashObj.update(pw)
        postPw = hashObj.hexdigest()
        writeFile(usr,postPw)
        readFile()
        return render_template("register_success.html")

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
            return render_template("common.html",t="Success",mes="Successfully logged in!",p="/",m="'GET'",b="Return to Login")
        else:
            return render_template("common.html",t="Failed",mes="Incorrect Password!",p="/",m="'GET'",b="Return to Login")
    else:
        return render_template("common.html",t="Failed",mes="Username Doesn't Exist",p="/",m="'GET'",b="Return to Login")

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

