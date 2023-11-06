from flask import Flask ,render_template,request,redirect
import json
import random as rd
import time
timesTriedToEnter = 0
faildToEnterTimer = 30
numOfFails = 0
answers = [2,3,1,2,4,1]
quistionNumber = -1
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
    global quistionNumber
    quistionNumber += 1
    print(quistionNumber)
    quistion = quistions[quistionNumber].split(",")
    print(quistion)
    return render_template("game.html",
                            question = quistion[0],
                            answer1 = quistion[1],
                            answer2 = quistion[2],
                            answer3 = quistion[3],
                            answer4 = quistion[4])
@app.route("/startAgain",methods=["GET","POST"])
def startAgain():
    global quistionNumber
    quistionNumber += 1
    print(quistionNumber)
    quistion = quistions[quistionNumber].split(",")
    print(quistion)
    return render_template("game.html",
                            question = quistion[0],
                            answer1 = quistion[1],
                            answer2 = quistion[2],
                            answer3 = quistion[3],
                            answer4 = quistion[4])
def failed():
    global numOfFails , quistionNumber
    numOfFails += 1
    print(f"num of fails{numOfFails}")
    if numOfFails == 3:
        quistionNumber = -1
        numOfFails = 0
        return render_template("failed.html")
    return setUpPage()

@app.route("/quiz",methods=["GET","POST"])
def quiz():
    if request.method == "POST":
        if timesTriedToEnter != 3:
            if request.form["email"].replace(" ","") != "" and request.form["password"].replace(" ","") != "":
                email = request.form["email"]
                password = request.form["password"]
                users[email] = password
                with open("users.json","w") as f:
                    json.dump(users,f)
                return setUpPage()
            else:
                timesTriedToEnter = timesTriedToEnter + 1
                return render_template("sigh_in.html")
        else:
            time.sleep(faildToEnterTimer)
            faildToEnterTimer = faildToEnterTimer*2
            timesTriedToEnter = 0

@app.route("/answer1",methods=["GET","POST"])
def answer1():
    if 1 == answers[quistionNumber]:
        return setUpPage()
    return failed()
@app.route("/answer2",methods=["GET","POST"])
def answer2():
    if 2 == answers[quistionNumber]:
        return setUpPage()
    return failed()
@app.route("/answer3",methods=["GET","POST"])
def answer3():
    if 3 == answers[quistionNumber]:
        return setUpPage()
    return failed()
@app.route("/answer4",methods=["GET","POST"])
def answer4():
    if 4 == answers[quistionNumber]:
        return setUpPage()
    return failed()
app.run()

