from flask import Flask, render_template, request
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
        return "<center>Please fill in all info!</center>"
    elif usr in data:
        return "<center>Username already exist!</center>"
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
            return "<center>Login Success!</center>"
        else:
            return "<center>Incorrect password!</center>"
    else:
        return "<center>User name doesn't exist!</center>"

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

