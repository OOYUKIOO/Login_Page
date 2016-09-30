from flask import Flask, render_template, request
import hashlib

app = Flask(__name__)

@app.route("/")
def home():
#    return render_template("login.html")
    return render_template("register.html")


@app.route("/register")

@app.route("/auth", methods=['POST'])
def loginCheck():
    print request.form["usr"]
    print request.form["pw"]
    if request.form["usr"] == "Mario" and request.form["pw"] == "12345":
        return "<center><b>Success!</b><center>"
    else:
        return "<center><b>Failure....</b><center>"

if __name__ == "__main__":
    app.debug = True
    app.run()

