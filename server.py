from flask import Flask ,render_template,request,redirect
import json
import random as rd
import time
import yagmail
contents : str
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
def log_on():
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
# @app.route("/restart",methods=["GET","POST"])
# def restart():
#     global quistionNumber
#     quistionNumber += 1
#     print(quistionNumber)
#     quistion = quistions[quistionNumber].split(",")
#     print(quistion)
#     return render_template("game.html",
#                             question = quistion[0],
#                             answer1 = quistion[1],
#                             answer2 = quistion[2],
#                             answer3 = quistion[3],
#                             answer4 = quistion[4])
def failed():
    global numOfFails , quistionNumber
    numOfFails += 1
    print(f"num of fails{numOfFails}")
    if numOfFails == 3:
        quistionNumber = -1
        numOfFails = 0
        return render_template("failed.html")
    if quistionNumber == 5 and numOfFails != 3:
        return render_template("win.html")
    return setUpPage()

@app.route("/quiz",methods=["GET","POST"])
def quiz():
    global faildToEnterTimer, timesTriedToEnter
    if request.method == "POST":
        if timesTriedToEnter != 2:
            if request.form["email"].replace(" ","") != "" and request.form["password"].replace(" ","") != "":
                email = request.form["email"]
                password = request.form["password"]
                if users[email] == password:
                
                    return setUpPage()
                else:
                    timesTriedToEnter = timesTriedToEnter + 1
                    print(timesTriedToEnter)
                    timesTriedToEnter = 0
                    faildToEnterTimer = 30
                    return render_template("sigh_in.html")
            else:
                return render_template("sigh_in.html")
        else:
            time.sleep(faildToEnterTimer)
            faildToEnterTimer = faildToEnterTimer*2
            timesTriedToEnter = 0
            return render_template("sigh_in.html")

def win():
    return render_template("win.html")

@app.route("/answer1",methods=["GET","POST"])
def answer1():
    if 1 == answers[quistionNumber]:
        if quistionNumber == 5:
            return win()
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

@app.route("/forgot_password",methods=["GET","POST"])
def getEmail():
    return render_template("recoverEmail.html")
@app.route("/send",methods=["GET","POST"])
def sendPassword():
    global contents
    if request.form["emailRecovered"].replace(" ","") != "":
        email = request.form["emailRecovered"].replace(" ","")
        contents = ""
        for i in range(6):
            contents  = contents + str(rd.randint(0,9))
        print(contents)
        return render_template("enterPinNumber.html")
    return render_template("recoverEmail.html")

@app.route("/recovered", methods=["POST","GET"])
def recover():
    global contents
    if request.form["enterPin"].replace(" ","") != "":
        if request.form["enterPin"].replace(" ","") == contents:
            return setUpPage()
    return render_template("enterPinNumber.html")
@app.route("/back",methods=["POST","GET"])
def back():
    return render_template("sigh_in.html")

@app.route("/exit",methods=["GET","POST"])
def exit():
    return exit()

@app.route("/restart",methods=["GET","POST"])
def restart():
    global numOfFails,timesTriedToEnter,faildToEnterTimer,quistionNumber
    numOfFails = 0
    timesTriedToEnter = 0
    faildToEnterTimer = 30
    quistionNumber = -1
    return render_template("sigh_in.html")

@app.route("/signin",methods=["POST","GET"])
def signin():
    return render_template("signin.html")
@app.route("/sigh_in",methods=["POST","GET"])
def sigh_in():
    if request.method == "POST":
        if (request.form["email"].replace(" ","") != "" and request.form["password"].replace(" ","") != ""):
            email = request.form["email"]
            password = request.form["password"]
            users[email] = password
            with open("users.json","w") as f:
                json.dump(users,f)
            return render_template("sigh_in.html")
        return render_template("signin.html")
        
                
app.run()

