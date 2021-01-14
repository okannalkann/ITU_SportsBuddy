from flask import Flask, abort, current_app, render_template, request, session, url_for, redirect, flash
import mysql.connector
from flask_mysqldb import MySQL
from database import Database
import bcrypt
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

from PIL import Image

import sys
import os
from werkzeug.utils import secure_filename

from flask_mail import Mail, Message


app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = r'.\static\images\users'
app.config["UPLOAD_SPORTS_SHARE_PHOTO"] = r'.\static\images\timeline\sports'
app.config["UPLOAD_GAMES_SHARE_PHOTO"] = r'.\static\images\timeline\games'
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ['JPG']


mail = Mail(app)
app.secret_key = "SportBuddy"
db = Database("127.0.0.1", 3306, "root", "qwerty123456", "mydb")
db.con.cursor()    

query = "SELECT * FROM mydb.website_mail"
db.cursor.execute(query)
site_mail = db.cursor.fetchone()

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = str(site_mail[1])
app.config['MAIL_PASSWORD'] = str(site_mail[2])
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route('/', methods=['GET','POST'])
def home_page():
    try:
        if 'user' in session:
            username = session['user']
            query="SELECT * FROM mydb.users"
            db.cursor.execute(query)
            myresult = db.cursor.fetchall()
            
            query="""SELECT mydb.games.game_id,mydb.games.game_name, mydb.game_has_category.game_category_cate_id FROM mydb.games
            LEFT JOIN mydb.game_has_category ON mydb.game_has_category.games_game_id = mydb.games.game_id
            WHERE mydb.game_has_category.game_category_cate_id = 15"""
            db.cursor.execute(query)
            actionGames = db.cursor.fetchall()
            actionGamesId=[]
            for i in actionGames: # converting int to string for void type error
                actionGamesId.append(str(i[0]))

            cateArray=[] #Category extract for every game card
            for i in actionGames:
                query="""SELECT mydb.game_category.category_name FROM mydb.game_category
                    LEFT JOIN mydb.game_has_category ON mydb.game_has_category.game_category_cate_id = mydb.game_category.cate_id
                    LEFT JOIN mydb.games ON mydb.games.game_id = mydb.game_has_category.games_game_id
                    WHERE mydb.games.game_id=""" + str(i[0])
                db.cursor.execute(query)
                cateler = db.cursor.fetchall()
                cateArray.append(cateler[0][0])

            query="""SELECT mydb.games.game_id,mydb.games.game_name, mydb.game_has_category.game_category_cate_id FROM mydb.games
            LEFT JOIN mydb.game_has_category ON mydb.game_has_category.games_game_id = mydb.games.game_id
            WHERE mydb.game_has_category.game_category_cate_id = 1"""
            db.cursor.execute(query)
            FPSGames = db.cursor.fetchall()

            FPSGamesId=[]
            for i in FPSGames: # converting int to string for void type error
                FPSGamesId.append(str(i[0]))

            FPSArray=[] #Category extract for every game card
            for i in FPSGames:
                query="""SELECT mydb.game_category.category_name FROM mydb.game_category
                    LEFT JOIN mydb.game_has_category ON mydb.game_has_category.game_category_cate_id = mydb.game_category.cate_id
                    LEFT JOIN mydb.games ON mydb.games.game_id = mydb.game_has_category.games_game_id
                    WHERE mydb.games.game_id=""" + str(i[0])
                db.cursor.execute(query)
                fps = db.cursor.fetchall()
                FPSArray.append(fps[0][0])
            
            query="""SELECT mydb.games.game_id,mydb.games.game_name, mydb.game_has_category.game_category_cate_id FROM mydb.games
            LEFT JOIN mydb.game_has_category ON mydb.game_has_category.games_game_id = mydb.games.game_id
            WHERE mydb.game_has_category.game_category_cate_id = 18"""
            db.cursor.execute(query)
            ShooterGames = db.cursor.fetchall()
            
            ShooterGamesId=[]
            for i in ShooterGames: # converting int to string for void type error
                ShooterGamesId.append(str(i[0]))

            ShooterArray=[] #Category extract for every game card
            for i in ShooterGames:
                query="""SELECT mydb.game_category.category_name FROM mydb.game_category
                    LEFT JOIN mydb.game_has_category ON mydb.game_has_category.game_category_cate_id = mydb.game_category.cate_id
                    LEFT JOIN mydb.games ON mydb.games.game_id = mydb.game_has_category.games_game_id
                    WHERE mydb.games.game_id=""" + str(i[0])
                db.cursor.execute(query)
                shooter = db.cursor.fetchall()
                ShooterArray.append(shooter[0][0])
 
            query="SELECT * FROM mydb.sports"
            db.cursor.execute(query)
            SportsTable = db.cursor.fetchall()
            
            SportsId=[]
            for i in SportsTable: # converting int to string for void type error
                SportsId.append(str(i[0]))
             
            
            return render_template('home.html',FPSArray=FPSArray,lenFPS=len(FPSArray),ShooterArray=ShooterArray,lenShooter=len(ShooterArray),lenCate=len(cateArray),cate=cateArray,SportsId=SportsId,SportsTable=SportsTable,ShooterGamesId=ShooterGamesId,FPSGamesId=FPSGamesId,actionGamesId=actionGamesId,ShooterGames=ShooterGames,FPSGames=FPSGames,actionGames=actionGames,lenSp=len(SportsTable),lenS=len(ShooterGames),lenF=len(FPSGames),lenA=len(actionGames),len=len(myresult), username=username)


        else:
            return redirect(url_for("login",haveto="You have to sign in"))
    except:
        print("hata")
    

@app.route('/sports', methods=['GET','POST'])
def sports():
    try:
        if 'user' in session:
            username = session['user'] 
            if request.method =="GET": #return values for button      
                query = "SELECT * FROM mydb.sports"
                db.cursor.execute(query)
                myresult = db.cursor.fetchall()
                myresult2=[]
                for i in myresult: # converting int to string for void type error
                    myresult2.append(str(i[0]))
                return render_template('sports.html',len=len(myresult),data=myresult,data2=myresult2,username=username)

        else:
            return redirect(url_for("login",haveto="You have to sign in"))
    except:
        print("Sport Page Error")

@app.route('/sports/<int:sport_id>', methods=['GET','POST'])
def sport_index(sport_id):
    try:
        if 'user' in session:
            username = session['user']
            Session_user_id = session['user_id']
            query="SELECT mydb.sports.sport_name FROM mydb.sports WHERE mydb.sports.sport_id= " + str(sport_id)
            db.cursor.execute(query)
            sport_name = db.cursor.fetchone()
            if request.method == "GET": #return values for button 
                query =""" 
                    SELECT mydb.users.user_name, mydb.users.user_surname, mydb.users.user_email, mydb.user_want_to_play_sports.User_description, mydb.user_want_to_play_sports.id_User_want_to_play_sports, mydb.users.user_id FROM mydb.users
                    LEFT JOIN mydb.user_want_to_play_sports ON mydb.users.user_id = mydb.user_want_to_play_sports.Users_user_id
                    LEFT JOIN mydb.sports ON mydb.user_want_to_play_sports.Sports_sport_id  = sports.sport_id
                    WHERE mydb.users.user_findingFriend = 1 and mydb.sports.sport_id = """
                db.cursor.execute(query + str(sport_id))
                myresult = db.cursor.fetchall()
                
                myresult2=[]
                for i in myresult: # converting int to string for void type error
                    myresult2.append(str(i[5]))
                

                query ="SELECT * FROM mydb.user_want_to_play_sports WHERE mydb.user_want_to_play_sports.sports_sport_id = "
                db.cursor.execute(query + str(sport_id))
                lenSportWish = db.cursor.fetchall()

                sport_id=str(sport_id)


                if myresult==[]:
                    yok="Nobody Wanted to Play :("
                    return render_template('sport_index.html',yok=yok,username=username,sport_ids=sport_id,sport_name=sport_name,lenSportWish=len(lenSportWish))
                
                return render_template('sport_index.html',len=len(myresult),data=myresult,data2=myresult2,username=username,
                sport_ids=sport_id,sport_name=sport_name,lenSportWish=len(lenSportWish))
            
            else:
                if request.form.get("add_request"):
                    user_description = request.form["email"] #request description
                    checkQuery="SELECT * FROM mydb.user_want_to_play_sports WHERE mydb.user_want_to_play_sports.users_user_id = " + str(Session_user_id)
                    checkQuery += " and mydb.user_want_to_play_sports.sports_sport_id = " + str(sport_id)
                    db.cursor.execute(checkQuery)
                    IsRecordExist = db.cursor.fetchone()
                    if IsRecordExist == None:  # add new sport request 
                        query="INSERT INTO mydb.user_want_to_play_sports (User_description, users_user_id, sports_sport_id) VALUES (%s,%s,%s)"
                        val = (user_description,Session_user_id,sport_id)
                        db.cursor.execute(query, val) #added the database
                        db.con.commit()
                    else: # if this else run this mean user already create sport request for this sport.
                          # He can not again more than one spor request 
                        query =""" 
                            SELECT mydb.users.user_name, mydb.users.user_surname, mydb.users.user_email, mydb.user_want_to_play_sports.User_description, mydb.users.user_id FROM mydb.users
                            LEFT JOIN mydb.user_want_to_play_sports ON mydb.users.user_id = mydb.user_want_to_play_sports.Users_user_id
                            LEFT JOIN mydb.sports ON mydb.user_want_to_play_sports.Sports_sport_id  = sports.sport_id
                            WHERE mydb.users.user_findingFriend = 1 and mydb.sports.sport_id = """
                        db.cursor.execute(query + str(sport_id))
                        myresult = db.cursor.fetchall()
                        return render_template('sport_index.html',len=len(myresult),data=myresult,username=username,sport_ids=sport_id,sport_name=sport_name,haveto="You already created request.")

                    

                return redirect(url_for("sport_index",sport_id=sport_id))
        else:
            return redirect(url_for("login",haveto="You have to sign in"))
    except:
        print("sport_index error")


@app.route('/sports/<int:sport_id>/<int:id_User_want_to_play_sports>', methods=['GET','POST'])
def contact(sport_id,id_User_want_to_play_sports):
    try:
        if 'user' in session:

            username = session['user']
            Session_user_id = session['user_id']
            query="SELECT mydb.sports.sport_name FROM mydb.sports WHERE mydb.sports.sport_id= " + str(sport_id)
            db.cursor.execute(query)
            sport_name = db.cursor.fetchone()

            if request.method == "GET": #return values for button 
                query="""SELECT mydb.users.user_name, mydb.users.user_surname, mydb.users.user_email, mydb.user_want_to_play_sports.User_description, mydb.users.user_id  FROM mydb.user_want_to_play_sports 
                    LEFT JOIN mydb.users ON mydb.user_want_to_play_sports.users_user_id = mydb.users.user_id
                    WHERE  mydb.users.user_findingFriend = 1 and mydb.user_want_to_play_sports.id_User_want_to_play_sports = """+ str(id_User_want_to_play_sports) # USer_id yanlis geliyor sessiondaki id ile aynı degilse patlıyo
                db.cursor.execute(query)
                myresult = db.cursor.fetchone()

                myresult2 = str(myresult[4])
                
                query =""" 
                    SELECT mydb.sport_request_messages.request_messages, mydb.users.user_name, mydb.users.user_surname, mydb.users.user_email, mydb.users.user_id  FROM mydb.sport_request_messages 
                    LEFT JOIN mydb.users ON mydb.sport_request_messages.users_user_id = mydb.users.user_id
                    WHERE mydb.sport_request_messages.user_want_to_play_sports_id_User_want_to_play_sports = """+str(id_User_want_to_play_sports)
                db.cursor.execute(query)
                mycomment = db.cursor.fetchall()
                print("asdakd,", mycomment)
                mycomment2=[]
                for i in mycomment: # converting int to string for void type error
                    mycomment2.append(str(i[4]))
                


                if mycomment ==[]:
                    print("Mycomment is empty")
                    return render_template('contact.html',data=myresult,data2=myresult2,username=username,sport_ids=sport_id,sport_name=sport_name,wantid=id_User_want_to_play_sports)
                else:
                    return render_template('contact.html',data=myresult,data2=myresult2,data3=mycomment2,lenRequestAnswer=len(mycomment),RequestAnswer=mycomment,username=username,sport_ids=sport_id,sport_name=sport_name,wantid=id_User_want_to_play_sports)
            else:
                if request.form.get("add_comment"):
                    user_description = request.form["email"] #request 
                    query="INSERT INTO mydb.sport_request_messages ( request_messages, user_want_to_play_sports_id_User_want_to_play_sports, users_user_id, sports_sport_id) VALUES (%s,%s,%s, %s)"
                    val = (user_description,id_User_want_to_play_sports,Session_user_id,sport_id)
                    db.cursor.execute(query, val) #added the database
                    db.con.commit()
                    return redirect(url_for("contact",sport_id=sport_id,id_User_want_to_play_sports=id_User_want_to_play_sports))
            
        else:
            return redirect(url_for("login",haveto="You have to sign in"))
    except:
        print("contact hata")


@app.route('/games', methods=['GET','POST'])
def games():
    try:
        if 'user' in session:
            username = session['user'] 
            if request.method =="GET": #return values for button      
                query = "SELECT * FROM mydb.games"
                db.cursor.execute(query)
                myresult = db.cursor.fetchall()
                myresult2=[]
                for i in myresult: # converting int to string for void type error
                    myresult2.append(str(i[0]))
                
                GameArray=[] #Category extract for every game card
                for i in myresult:
                    query="""SELECT mydb.game_category.category_name FROM mydb.game_category
                        LEFT JOIN mydb.game_has_category ON mydb.game_has_category.game_category_cate_id = mydb.game_category.cate_id
                        LEFT JOIN mydb.games ON mydb.games.game_id = mydb.game_has_category.games_game_id
                        WHERE mydb.games.game_id=""" + str(i[0])
                    db.cursor.execute(query)
                    gameTypes = db.cursor.fetchall()
                    GameArray.append(gameTypes[0][0])


                query = "SELECT * FROM mydb.game_category"
                db.cursor.execute(query)
                AllCategories = db.cursor.fetchall()
                    
    
                return render_template('games.html',lenAll=len(AllCategories),listCate=AllCategories,GameArray=GameArray,lenG=len(GameArray),len=len(myresult),data=myresult,data2=myresult2,username=username)
            if request.method =="POST":
                game_type = request.form.get('categories')
                if game_type == "All":
                    return redirect(url_for("games"))
                else:
                    query = "SELECT * FROM mydb.game_category WHERE mydb.game_category.category_name = %s"
                    db.cursor.execute(query,(game_type,))
                    categoryid = db.cursor.fetchone()

                query = """SELECT mydb.games.game_id, mydb.games.game_name FROM mydb.game_has_category
                    LEFT JOIN mydb.games ON  mydb.games.game_id = mydb.game_has_category.games_game_id
                    LEFT JOIN mydb.game_category ON mydb.game_category.cate_id = mydb.game_has_category.game_category_cate_id
                    WHERE mydb.game_category.cate_id = %s"""
                db.cursor.execute(query,(categoryid[0],))
                categoryGame = db.cursor.fetchall()

                gameType=[]
                for i in categoryGame: # converting int to string for void type error
                    gameType.append(str(game_type))
                
                myresult2=[]
                for i in categoryGame: # converting int to string for void type error
                    myresult2.append(str(i[0]))
                
                query = "SELECT * FROM mydb.game_category"
                db.cursor.execute(query)
                AllCategories = db.cursor.fetchall()
  
                return render_template('games.html',lenAll=len(AllCategories),listCate=AllCategories,GameArray=gameType,lenG=len(categoryGame),len=len(categoryGame),data=categoryGame,data2=myresult2,username=username)
            
        else:
            return redirect(url_for("login"))
    except:
        print("Games Page Error")


@app.route('/games/<int:game_id>', methods=['GET','POST'])
def game_index(game_id):
    try:
        if 'user' in session:
            username = session['user']
            Session_user_id = session['user_id']
            query="SELECT mydb.games.game_name FROM mydb.games WHERE mydb.games.game_id= " + str(game_id)
            db.cursor.execute(query)
            game_name = db.cursor.fetchone()
            if request.method == "GET": #return values for button 
                query =""" 
                    SELECT mydb.users.user_name, mydb.users.user_surname, mydb.users.user_email, mydb.user_want_to_play_games.User_description, mydb.user_want_to_play_games.id_user_want_to_play_games, mydb.users.user_id FROM mydb.users
                    LEFT JOIN mydb.user_want_to_play_games ON mydb.users.user_id = mydb.user_want_to_play_games.users_user_id
                    LEFT JOIN mydb.games ON mydb.user_want_to_play_games.games_game_id  = games.game_id
                    WHERE mydb.users.user_findingFriend = 1 and mydb.games.game_id = """
                db.cursor.execute(query + str(game_id))
                myresult = db.cursor.fetchall()
                myresult2=[]
                for i in myresult: # converting int to string for void type error
                    myresult2.append(str(i[5]))
                
                game_id=str(game_id)


                query =""" 
                SELECT mydb.game_category.category_name FROM mydb.game_has_category 
                LEFT JOIN mydb.game_category ON mydb.game_category.cate_id = mydb.game_has_category.game_category_cate_id
                WHERE game_has_category.games_game_id =
                """
                db.cursor.execute(query + str(game_id))
                game_cate = db.cursor.fetchall()


                query ="SELECT * FROM mydb.user_want_to_play_games WHERE mydb.user_want_to_play_games.games_game_id = "
                db.cursor.execute(query + str(game_id))
                lenGameWish = db.cursor.fetchall()

                

                if myresult==[]:
                    yok="Nobody Wanted to Play :("
                    return render_template('game_index.html',yok=yok,username=username,game_ids=game_id,
                    game_name=game_name,categories=game_cate,lenCate=len(game_cate),lenGameWish=len(lenGameWish))

                return render_template('game_index.html',len=len(myresult),data=myresult,data2=myresult2,
                username=username,game_ids=game_id,game_name=game_name,categories=game_cate,lenCate=len(game_cate),lenGameWish=len(lenGameWish))
            
            else:
                if request.form.get("add_request"):
                    user_description = request.form["email"] #request description
                    checkQuery="SELECT * FROM mydb.user_want_to_play_games WHERE mydb.user_want_to_play_games.users_user_id = " + str(Session_user_id)
                    checkQuery += " and mydb.user_want_to_play_games.games_game_id = " + str(game_id)
                    db.cursor.execute(checkQuery)
                    IsRecordExist = db.cursor.fetchone()
                    if IsRecordExist == None:  # add new game request 
                        query="INSERT INTO mydb.user_want_to_play_games (User_description, users_user_id, games_game_id) VALUES (%s,%s,%s)"
                        val = (user_description,Session_user_id,game_id)
                        db.cursor.execute(query, val) #added the database
                        db.con.commit()
                    else: # if this else run this mean user already create game request for this sport.
                          # He can not again more than one game request 
                        query =""" 
                            SELECT mydb.users.user_name, mydb.users.user_surname, mydb.users.user_email, mydb.user_want_to_play_games.User_description, mydb.users.user_id FROM mydb.users
                            LEFT JOIN mydb.user_want_to_play_games ON mydb.users.user_id = mydb.user_want_to_play_games.users_user_id
                            LEFT JOIN mydb.games ON mydb.user_want_to_play_games.games_game_id = games.game_id
                            WHERE mydb.users.user_findingFriend = 1 and mydb.games.game_id = """
                        db.cursor.execute(query + str(game_id))
                        myresult = db.cursor.fetchall()
                        myresult2=[]
                        for i in myresult: # converting int to string for void type error
                            myresult2.append(str(i[4]))
                        
                        return render_template('game_index.html',len=len(myresult),data=myresult,data2=myresult2,username=username,game_ids=game_id,game_name=game_name,haveto="You already created request.")

                    

                return redirect(url_for("game_index",game_id=game_id))
        else:
            return redirect(url_for("login",haveto="You have to sign in"))
    except:
        print("game_index hata")


@app.route('/games/<int:game_id>/<int:id_user_want_to_play_games>', methods=['GET','POST'])
def game_contact(game_id,id_user_want_to_play_games):
    try:
        if 'user' in session:
            username = session['user']
            Session_user_id = session['user_id']
            query="SELECT mydb.games.game_name FROM mydb.games WHERE mydb.games.game_id= " + str(game_id)
            db.cursor.execute(query)
            game_name = db.cursor.fetchone()
            if request.method == "GET": #return values for button 
                query="""SELECT mydb.users.user_name, mydb.users.user_surname, mydb.users.user_email, mydb.user_want_to_play_games.User_description, mydb.users.user_id  FROM mydb.user_want_to_play_games 
                    LEFT JOIN mydb.users ON mydb.user_want_to_play_games.users_user_id = mydb.users.user_id
                    WHERE  mydb.users.user_findingFriend = 1 and mydb.user_want_to_play_games.id_user_want_to_play_games ="""+ str(id_user_want_to_play_games) # USer_id yanlis geliyor sessiondaki id ile aynı degilse patlıyo
                db.cursor.execute(query)
                myresult = db.cursor.fetchone()

                myresult2 = str(myresult[4])
                

                query =""" SELECT mydb.games_request_messages.games_request_messages, mydb.users.user_name, mydb.users.user_surname, mydb.users.user_email, mydb.users.user_id  FROM mydb.games_request_messages 
                    LEFT JOIN mydb.users ON mydb.games_request_messages.users_user_id = mydb.users.user_id
                    WHERE mydb.games_request_messages.user_want_to_play_games_id_user_want_to_play_games = """+str(id_user_want_to_play_games)
                db.cursor.execute(query)
                mycomment = db.cursor.fetchall()

                mycomment2=[]
                for i in mycomment: # converting int to string for void type error
                    mycomment2.append(str(i[4]))
                
                if mycomment ==[]:
                    print("Mycomment is empty")
                    return render_template('game_contact.html',data=myresult,data2=myresult2,username=username,game_name=game_name,wantid=id_user_want_to_play_games)
                else:
                    print("Mycomment is not empty")
                    return render_template('game_contact.html',data=myresult,data2=myresult2,data3=mycomment2,lenRequestAnswer=len(mycomment),RequestAnswer=mycomment,username=username,game_name=game_name,wantid=id_user_want_to_play_games)
            else:
                if request.form.get("add_comment"):
                    user_description = request.form["email"] #request 
                    query="INSERT INTO mydb.games_request_messages ( games_request_messages, user_want_to_play_games_id_user_want_to_play_games, users_user_id, games_game_id) VALUES (%s,%s,%s, %s)"
                    val = (user_description,id_user_want_to_play_games,Session_user_id,game_id)
                    db.cursor.execute(query, val) #added the database
                    db.con.commit()
                    return redirect(url_for("game_contact",game_id=game_id,id_user_want_to_play_games=id_user_want_to_play_games))
            
        else:
            return redirect(url_for("login",haveto="You have to sign in"))
    except:
        print("Game Contact hata")


def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False


@app.route('/profile', methods=['GET','POST'])
def profile():
    try:
        if 'user' in session:
            username = session['user'] 
            user_id = session['user_id']
            query = "SELECT * FROM mydb.users where mydb.users.user_id= " + str(user_id)
            db.cursor.execute(query)
            myresult = db.cursor.fetchone()
            print("my", myresult[0])
            myresult2 = str(myresult[0])
            ff = myresult[6]
            if ff==1:
                ff_send = "Yes"
            else:
                ff_send = "No"
            
            query="""SELECT mydb.user_want_to_play_games.User_description, mydb.users.user_id, mydb.games.game_name FROM mydb.user_want_to_play_games
            LEFT JOIN mydb.games ON mydb.games.game_id = mydb.user_want_to_play_games.games_game_id
            LEFT JOIN mydb.users ON mydb.users.user_id = mydb.user_want_to_play_games.users_user_id
            WHERE users_user_id = """+ str(user_id)
            db.cursor.execute(query)
            allUserPost = db.cursor.fetchall()
            UserPI=[]
            for i in allUserPost:
                UserPI.append(str(i[1]))

            query="""SELECT mydb.user_want_to_play_sports.User_description, mydb.users.user_id, mydb.sports.sport_name FROM mydb.user_want_to_play_sports
            LEFT JOIN mydb.sports ON mydb.sports.sport_id = mydb.user_want_to_play_sports.sports_sport_id
            LEFT JOIN mydb.users ON mydb.users.user_id = mydb.user_want_to_play_sports.users_user_id
            WHERE users_user_id = """+ str(user_id)
            db.cursor.execute(query)
            allUserSportPost = db.cursor.fetchall()
            UserSportPI=[]
            for i in allUserSportPost:
                UserSportPI.append(str(i[1]))

            if request.method =="GET": #return values for button      
                return render_template('profile.html',data=myresult,data2=myresult2,username=username,
                ff_send=ff_send,allUserPost=allUserPost,lenallUserPost=len(allUserPost),UserPI=UserPI,UserSportPI=UserSportPI,
                allUserSportPost=allUserSportPost,lenallUserSportPost=len(allUserSportPost))
            else:
                if request.form.get("edit_profile"):
                    name = request.form["name"]
                    surname = request.form["surname"]
                    school_number = request.form["school_number"]
                    email = request.form["email"]
                    pswrd = request.form["password"].encode('utf-8')
                    hash_password = bcrypt.hashpw(pswrd,bcrypt.gensalt())
                    query= (" UPDATE mydb.users SET user_name= %s, user_surname= %s, user_schoolNumber = %s, user_email = %s, user_password = %s WHERE (user_id = %s) ")
                    val=(name,surname,school_number,email,hash_password,user_id)
                    db.cursor.execute(query, val) #added the database
                    db.con.commit()
                    return redirect(url_for("profile"))

                if request.form.get("change_findfriend"):
                    if ff==1:
                        query= " UPDATE mydb.users SET mydb.users.user_findingFriend = 0 WHERE mydb.users.user_id ="+str(user_id)
                        db.cursor.execute(query)
                        db.con.commit()
                    else:
                        query= " UPDATE mydb.users SET mydb.users.user_findingFriend = 1 WHERE mydb.users.user_id = "+str(user_id)
                        db.cursor.execute(query)
                        db.con.commit()
                    return redirect(url_for("profile"))
                if request.form.get("uphoto"):

                    image = request.files["file"]
                    

                    if image.filename == "":
                        print("No filename")
                        return redirect(url_for("profile"))

                    if allowed_image(image.filename):
                        filename= str(user_id) +".jpg"
                        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        return redirect(url_for("profile"))

                    else:
                        print("That file extension is not allowed")
                        return redirect(url_for("profile"))
                if request.form.get("changepassword"):
                    oldpassword = request.form["oldpassword"].encode('utf-8')
                    newpassword = request.form["password"].encode('utf-8')
                    cnewpassword = request.form["cpassword"].encode('utf-8')

                    if newpassword != cnewpassword:
                        flash("Password not matched","info")
                        return redirect(url_for("profile"))

                    email=session['user_email']

                    query = "SELECT * FROM mydb.users WHERE user_email =\"" + email + "\""
                    db.cursor.execute(query)
                    myresult = db.cursor.fetchone()
                    if myresult is None:
                        return redirect(url_for("login"))
                    if bcrypt.hashpw(oldpassword,myresult[5].encode('utf-8') ) == myresult[5].encode('utf-8'):
                        hash_password = bcrypt.hashpw(newpassword,bcrypt.gensalt())
                        query= (" UPDATE mydb.users SET user_password = %s WHERE (user_id = %s) ")
                        val=(hash_password,user_id)
                        db.cursor.execute(query, val) #added the database
                        db.con.commit()
                        flash('Password has been changed.', 'info')
                    else:
                        flash('Password did not changed.', 'info')
                    return redirect(url_for("profile"))

                if request.form.get("getpost"):                 
                    print("delee")
                    allp = request.form["posttype"]
                    if allp=="allpost":
                        print("@@@@@@@@@@@@@@@@")
                        return redirect(url_for("profile"))
                    if allp=="games":
                        query="""SELECT mydb.user_want_to_play_games.User_description, mydb.users.user_id, mydb.games.game_name FROM mydb.user_want_to_play_games
                        LEFT JOIN mydb.games ON mydb.games.game_id = mydb.user_want_to_play_games.games_game_id
                        LEFT JOIN mydb.users ON mydb.users.user_id = mydb.user_want_to_play_games.users_user_id
                        WHERE users_user_id = """+ str(user_id)
                        db.cursor.execute(query)
                        allUserPost = db.cursor.fetchall()
                        UserPI=[]
                        for i in allUserPost:
                            UserPI.append(str(i[1]))

                        return render_template('profile.html',data=myresult,data2=myresult2,username=username,
                        ff_send=ff_send,allUserPost=allUserPost,lenallUserPost=len(allUserPost),UserPI=UserPI)
                    if allp=="sports":
                        query="""SELECT mydb.user_want_to_play_sports.User_description, mydb.users.user_id, mydb.sports.sport_name FROM mydb.user_want_to_play_sports
                        LEFT JOIN mydb.sports ON mydb.sports.sport_id = mydb.user_want_to_play_sports.sports_sport_id
                        LEFT JOIN mydb.users ON mydb.users.user_id = mydb.user_want_to_play_sports.users_user_id
                        WHERE users_user_id = """+ str(user_id)
                        db.cursor.execute(query)
                        allUserPost = db.cursor.fetchall()
                        UserPI=[]
                        for i in allUserPost:
                            UserPI.append(str(i[1]))

                        return render_template('profile.html',data=myresult,data2=myresult2,username=username,
                        ff_send=ff_send,allUserPost=allUserPost,lenallUserPost=len(allUserPost),UserPI=UserPI)

                        
                    
        else:
            return redirect(url_for("login"))
    except:
        print("Profil Sayfa hatası")


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('error.html'), 404

@app.route('/timeline', methods=['GET','POST'])
def timeline():
    try:
        if 'user' in session:
            username = session['user']
            user_id=session['user_id']
            if request.method=="GET":

                #POST SPORT
                query="""SELECT mydb.shared_sport_photos.shared_sport_photo_id, mydb.shared_sport_photos.sport_description, mydb.users.user_name, mydb.users.user_surname, mydb.users.user_id, mydb.sports.sport_name, mydb.shared_sport_photos.photo_reference FROM mydb.shared_sport_photos
                    LEFT JOIN mydb.users ON mydb.users.user_id = mydb.shared_sport_photos.users_user_id
                    LEFT JOIN mydb.sports ON mydb.sports.sport_id = mydb.shared_sport_photos.sports_sport_id"""
                db.cursor.execute(query)
                Alltimeline = db.cursor.fetchall()


                photoId=[]
                for i in Alltimeline: # converting int to string for void type error
                    photoId.append(str(i[4]))
                
                SharedPhotoId=[]
                for i in Alltimeline: # converting int to string for void type error
                    SharedPhotoId.append(str(i[6]))
                
                query = "SELECT * FROM mydb.sports"
                db.cursor.execute(query)
                AllSports = db.cursor.fetchall()

                # POST GAME

                query="""SELECT mydb.shared_game_photos.shared_game_photo_id, mydb.shared_game_photos.photo_description, mydb.users.user_name, mydb.users.user_surname, mydb.users.user_id, mydb.games.game_name, mydb.shared_game_photos.photo_reference FROM mydb.shared_game_photos
                LEFT JOIN mydb.users ON mydb.users.user_id = mydb.shared_game_photos.users_user_id
                LEFT JOIN mydb.games ON mydb.games.game_id = mydb.shared_game_photos.games_game_id"""
                db.cursor.execute(query)
                AllGametimeline = db.cursor.fetchall()


                GamephotoId=[]
                for i in AllGametimeline: # converting int to string for void type error
                    GamephotoId.append(str(i[4]))
                
                SharedGamePhotoId=[]
                for i in AllGametimeline: # converting int to string for void type error
                    SharedGamePhotoId.append(str(i[6]))
                
                query = "SELECT * FROM mydb.games"
                db.cursor.execute(query)
                AllGames = db.cursor.fetchall()

                return render_template("timeline.html",data=Alltimeline,lenAll=len(Alltimeline),data2=photoId,
                data3=SharedPhotoId,username=username,Sports=AllSports,lenSports=len(AllSports),
                gameData=AllGametimeline,lengameData=len(AllGametimeline),GamePhotoId=GamephotoId,
                SharedGamePhotoId=SharedGamePhotoId,Games=AllGames,lenGames=len(AllGames) )



            else:
                if request.form.get("sharePhoto"):

                    description = request.form['description']
                    
                    image = request.files["file"]
                    
                    if image.filename == "":
                        print("No filename")
                        return redirect(url_for("timeline"))

                    postType= request.form.get('postType')
                    if postType == "GameType":
                        typePost = request.form.get('game_categories')
                        query = "SELECT * FROM mydb.games where game_name=%s"
                        db.cursor.execute(query,(typePost,))
                        game_id = db.cursor.fetchone()
                        print(typePost,game_id)
                        max = sys.maxsize
                        photo_id=0
                        k=1
                        while(k<max):
                            query="SELECT * FROM mydb.shared_game_photos WHERE photo_reference =%s"
                            db.cursor.execute(query,(k,))
                            reference_id = db.cursor.fetchone()
                            if reference_id==None:
                                photo_id=k
                                break
                            k+=1
#""" Pummel parti baya eğlenceliydi. Bidahakine sizi de bekleriz :)) @tiras16 @irtegunk16 @yaylali16 @alkano @dursune16 @arslanru16 """
                        print(k,photo_id)
                        print(description,user_id,game_id[0],photo_id)
                        query="INSERT INTO mydb.shared_game_photos (photo_description, users_user_id, games_game_id, photo_reference) VALUES (%s,%s, %s, %s)"
                        val = (description,user_id,game_id[0],photo_id)
                        
                        db.cursor.execute(query,val)
                        db.con.commit()
                        print("como")
                        if allowed_image(image.filename):
                            filename= str(photo_id) +".jpg"
                            image.save(os.path.join(app.config['UPLOAD_GAMES_SHARE_PHOTO'], filename))

                    elif postType == "SportType":
                        typePost = request.form.get('sport_categories')
                        query = "SELECT * FROM mydb.sports where sport_name=%s"
                        db.cursor.execute(query,(typePost,))
                        sport_id = db.cursor.fetchone()
                        
                        max = sys.maxsize
                        photo_id=0
                        k=1
                        while(k<max):
                            query="SELECT * FROM mydb.shared_sport_photos WHERE photo_reference =%s"
                            db.cursor.execute(query,(k,))
                            reference_id = db.cursor.fetchone()
                            if reference_id==None:
                                photo_id=k
                                break
                            k+=1

                        query="INSERT INTO mydb.shared_sport_photos (sport_description, users_user_id, sports_sport_id, photo_reference) VALUES (%s,%s, %s, %s)"
                        val = (description,user_id,sport_id[0],photo_id)
                        
                        db.cursor.execute(query,val)
                        db.con.commit()

                        if allowed_image(image.filename):
                            filename= str(photo_id) +".jpg"
                            image.save(os.path.join(app.config['UPLOAD_SPORTS_SHARE_PHOTO'], filename))
                        

                    return redirect(url_for("timeline"))
        else:
            return redirect(url_for("login"))
    except:
        print("Timeline Page Error")

@app.route('/login', methods=['GET','POST'])
def login():
    try:
        if request.method == "POST": 
            session.permanent = True
            if request.form.get("login-button"):
                user_email = request.form["username"] #take username from website textbox
                user_password = request.form["password"].encode('utf-8') #take password from website textbox
                query = "SELECT * FROM mydb.users WHERE user_email =\"" + user_email + "\""
                db.cursor.execute(query)
                Logincheck = db.cursor.fetchone()
                if Logincheck:
                    #if Logincheck[5] == user_password: # check password
                    if bcrypt.hashpw(user_password,Logincheck[5].encode('utf-8') ) == Logincheck[5].encode('utf-8'):
                        session["user"] = Logincheck[1]
                        session["user_id"] = Logincheck[0]
                        session["user_email"] = Logincheck[4]
                        return redirect(url_for("home_page"))

                    else:
                        return render_template("login.html",haveto="Wrong Account")

                else:
                    return render_template("login.html",haveto="Wrong Account")

            if request.form.get("sign_up"):
                newUser_name = request.form["name"] #take username from website textbox
                newUser_surname = request.form["surname"] #take password from website textbox
                newUser_school_number = request.form["school_number"] #take username from website textbox
                newUser_password = request.form["password"].encode('utf-8') #take password from website textbox
                newUser_confirmpassword = request.form["cpassword"].encode('utf-8') #take username from website textbox
                newUser_email = request.form["email"] #take password from website textbox
                if newUser_password != newUser_confirmpassword:
                    return render_template("login.html",haveto="Password Not Matched")
                
                hash_password = bcrypt.hashpw(newUser_password,bcrypt.gensalt())
                query = "SELECT * FROM mydb.users WHERE user_email =\"" + newUser_email + "\""
                db.cursor.execute(query)
                check_email= db.cursor.fetchone()
                if check_email != None:
                    return render_template("login.html",haveto="This e-mail already registered.")
                else:
                    query="INSERT INTO mydb.users (user_name, user_surname, user_schoolNumber, user_email, user_password, user_findingFriend) VALUES (%s,%s,%s,%s,%s,%s)"
                    val = (newUser_name,newUser_surname,newUser_school_number,newUser_email,hash_password,"1")
                    db.cursor.execute(query, val) #added the database
                    db.con.commit()
                
        else:
            if "user" in session: #if already logged, redirect
                user_email=session["user"]
                return redirect(url_for("home_page"))

        return render_template("login.html")
    except:
        print("Login Error")


@app.route("/logout")
def logout():
    session.pop("user", None) #logout
    return redirect(url_for("login"))


def send_reset_email(user_email):
    query="SELECT * FROM mydb.users WHERE mydb.users.user_email=%s"
    db.cursor.execute(query,(user_email,))
    user = db.cursor.fetchone()
    token = get_reset_token(user[0])
    msg = Message('Password Reset Request',
                  sender='no.reply.sportsbuddy@gmail.com',
                  recipients=[user_email])
    msg.body = f'''To reset your password, visit the following link:
            {url_for('reset_token', token=token, _external=True)}
            If you did not make this request then simply ignore this email and no changes will be made.
            '''
    mail.send(msg)

def get_reset_token(user_id, expires_sec=1800):        
    s = Serializer(app.config['SECRET_KEY'], expires_sec)
    return s.dumps({'user_id': user_id}).decode('utf-8')

def verify_reset_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        tuser_id = s.loads(token)['user_id']
    except:
        return None
    query="SELECT * FROM mydb.users WHERE mydb.users.user_id=%s"
    db.cursor.execute(query,(tuser_id,))
    user = db.cursor.fetchone()
    return user
    

@app.route("/reset_request", methods=['GET', 'POST'])
def reset_request():
    try:
        if request.method =="GET": #return values for button      
            return render_template('reset_request.html')
        if request.method =="POST":
            if request.form.get("send_Emailrequest"):
                email = request.form["email"]
                send_reset_email(email)
                flash('An email has been sent with instructions to reset your password.', 'info')
                return redirect(url_for('login'))
    except:
        print("Reset Pw Error")


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    try:
        user = verify_reset_token(token)
        if user is None:
            flash('That is an invalid or expired token', 'warning')
            return redirect(url_for('reset_request'))


        if request.method =="GET": #return values for button      
            return render_template('reset_token.html')
            

        if request.method =="POST": #return values for button      
            if request.form.get("update_password"):
                pw=request.form["password"].encode('utf-8')
                cpw= request.form["cpassword"].encode('utf-8')
                if pw != cpw:
                    flash('Your password not matched!', 'success')
                    return redirect(url_for('reset_token',token=token))
                hashed_password = bcrypt.hashpw(pw,bcrypt.gensalt())
                query= (" UPDATE mydb.users SET user_password = %s WHERE (user_id = %s) ")
                val=(hashed_password,user[0])
                db.cursor.execute(query, val) #added the database
                db.con.commit()
                flash('Your password has been updated! You are now able to log in', 'success')
                return redirect(url_for('login'))

    except:
        print("Reset Pw Error")

if __name__ == '__main__':
    app.run(debug=True)
