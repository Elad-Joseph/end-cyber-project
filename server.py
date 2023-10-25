from flask import Flask ,render_template,request,redirect
import json
import random as rd
usedQustions = []
app = Flask(__name__,template_folder="template")
with open("quistions.text", "r")as fo:
    quistions = fo.readlines()
    numberOfRows = len(fo.readlines())
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
            quistionNumber = rd.randint(0,len(quistions)-1)
            usedQustions.append(quistionNumber)
            quistion = quistions[quistionNumber].split(",")
            print(quistion)
            return render_template("game.html",
                                   question = quistion[0],
                                   answer1 = quistion[1],
                                   answer2 = quistion[2],
                                   answer3 = quistion[3],
                                   answer4 = quistion[4])
        else:
            return render_template("sigh_in.html")


app.run()