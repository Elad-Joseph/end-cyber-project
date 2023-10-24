from flask import Flask ,render_template,request,redirect
import json

app = Flask(__name__,template_folder="template")

with open("users.json","r") as f:
    users = json.load(f)

@app.route("/")
def sigh_in():
    return render_template("sigh_in.html")

@app.route("/quiz",methods=["GET","POST"])
def quiz():
    if request.method == "POST":
        if request.form["email"].replace(" ","") != "" and request.form["password"].replace(" ","") != "":
            email = request.form["email"]
            password = request.form["password"]
            users[email] = password
            with open("users.json","w") as f:
                json.dump(users,f)
            return render_template("game.html")
        else:
            return render_template("sigh_in.html")
        

app.run()