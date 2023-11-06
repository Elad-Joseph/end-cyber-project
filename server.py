from flask import Flask ,render_template,request,redirect
import json
import random as rd
usedQustions = []
answers = [2,3,1,2,4,1]
quistionNumber : int
app = Flask(__name__,template_folder="template")
with open("quistions.text", "r")as fo:
    quistions = fo.readlines()
    numberOfRows = len(fo.readlines())
with open("users.json","r") as f:
    users = json.load(f)

@app.route("/")
def sigh_in():
    return render_template("sigh_in.html")

def setUpPage():
    # quistionNumber = -1
    # print(len(quistions))
    # while quistionNumber not in usedQustions: 
    #     quistionNumber = rd.randint(0,len(quistions)-1)
    # quistionNumber = 6
    # usedQustions.append(quistionNumber)
    quistion = quistions[6].split(",")
    return render_template("game.html",
                            question = quistion[0],
                            answer1 = quistion[1],
                            answer2 = quistion[2],
                            answer3 = quistion[3],
                            answer4 = quistion[4])

@app.route("/quiz",methods=["GET","POST"])
def quiz():
    if request.method == "POST":
        if request.form["email"].replace(" ","") != "" and request.form["password"].replace(" ","") != "":
            email = request.form["email"]
            password = request.form["password"]
            users[email] = password
            with open("users.json","w") as f:
                json.dump(users,f)
                quistion = quistions[7].split(",")
                print(quistion)
                quistion[1] = str(quistion[1])
            return render_template("game.html",
                            question = quistion[0],
                            answer1 = quistion[1],
                            answer2 = quistion[2],
                            answer3 = quistion[3],
                            answer4 = quistion[4])
            # setUpPage()
        else:
            return render_template("sigh_in.html")

@app.route("/answer1",methods=["GET","POST"])
def answer1():
    if 1 == answers[quistionNumber]:
        setUpPage()

app.run()

