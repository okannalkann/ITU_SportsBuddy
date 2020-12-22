from flask import Flask, abort, current_app, render_template, request, session, url_for, redirect, flash
import mysql.connector
from flask_mysqldb import MySQL
from database import Database
import bcrypt

app = Flask(__name__)
app.secret_key = "SportBuddy"
db = Database("127.0.0.1", 3306, "root", "qwerty123456", "mydb")
db.con.cursor()    


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
        print("Sport Sayfa hatası")

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
                    SELECT mydb.users.user_name, mydb.users.user_surname, mydb.users.user_email, mydb.user_want_to_play_sports.User_description, mydb.user_want_to_play_sports.id_User_want_to_play_sports FROM mydb.users
                    LEFT JOIN mydb.user_want_to_play_sports ON mydb.users.user_id = mydb.user_want_to_play_sports.Users_user_id
                    LEFT JOIN mydb.sports ON mydb.user_want_to_play_sports.Sports_sport_id  = sports.sport_id
                    WHERE mydb.users.user_findingFriend = 1 and mydb.sports.sport_id = """
                db.cursor.execute(query + str(sport_id))
                myresult = db.cursor.fetchall()
                
                if myresult==[]:
                    yok="Nobody Wanted to Play :("
                    return render_template('sport_index.html',yok=yok,username=username,sport_ids=sport_id,sport_name=sport_name)
                print("adasd",myresult)
                return render_template('sport_index.html',len=len(myresult),data=myresult,username=username,sport_ids=sport_id,sport_name=sport_name)
            
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
        print("sport_index hata")


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
                query="""SELECT mydb.users.user_name, mydb.users.user_surname, mydb.users.user_email, mydb.user_want_to_play_sports.User_description  FROM mydb.user_want_to_play_sports 
                    LEFT JOIN mydb.users ON mydb.user_want_to_play_sports.users_user_id = mydb.users.user_id
                    WHERE  mydb.users.user_findingFriend = 1 and mydb.user_want_to_play_sports.id_User_want_to_play_sports = """+ str(id_User_want_to_play_sports) # USer_id yanlis geliyor sessiondaki id ile aynı degilse patlıyo
                db.cursor.execute(query)
                myresult = db.cursor.fetchone()
                print("Myresult", myresult)
                query =""" 
                    SELECT mydb.sport_request_messages.request_messages, mydb.users.user_name, mydb.users.user_surname, mydb.users.user_email  FROM mydb.sport_request_messages 
                    LEFT JOIN mydb.users ON mydb.sport_request_messages.users_user_id = mydb.users.user_id
                    WHERE mydb.sport_request_messages.user_want_to_play_sports_id_User_want_to_play_sports = """+str(id_User_want_to_play_sports)
                db.cursor.execute(query)
                mycomment = db.cursor.fetchall()

                if mycomment ==[]:
                    print("Mycomment is empty")
                    return render_template('contact.html',data=myresult,username=username,sport_ids=sport_id,sport_name=sport_name,wantid=id_User_want_to_play_sports)
                else:
                    print("Mycomment is not empty")
                    return render_template('contact.html',data=myresult,lenRequestAnswer=len(mycomment),RequestAnswer=mycomment,username=username,sport_ids=sport_id,sport_name=sport_name,wantid=id_User_want_to_play_sports)
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
    
                return render_template('games.html',GameArray=GameArray,lenG=len(GameArray),len=len(myresult),data=myresult,data2=myresult2,username=username)
            # else:
            #     if request.form.get("game_types"):
            #         query = "SELECT * FROM mydb.game_category"
            #         db.cursor.execute(query)
            #         AllCategories = db.cursor.fetchall()

            #         # query = "SELECT * FROM mydb.game_category WHERE mydb.game_category.cate_id = %s"
            #         # val = LBCate_id
            #         # db.cursor.execute(query,LBCate_id)
            #         # categoryGame = db.cursor.fetchall()
            #         return redirect(url_for("games",listCate=AllCategories))
        else:
            return redirect(url_for("login",haveto="You have to sign in"))
    except:
        print("Games Sayfa hatası")


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
                    SELECT mydb.users.user_name, mydb.users.user_surname, mydb.users.user_email, mydb.user_want_to_play_games.User_description, mydb.user_want_to_play_games.id_user_want_to_play_games FROM mydb.users
                    LEFT JOIN mydb.user_want_to_play_games ON mydb.users.user_id = mydb.user_want_to_play_games.users_user_id
                    LEFT JOIN mydb.games ON mydb.user_want_to_play_games.games_game_id  = games.game_id
                    WHERE mydb.users.user_findingFriend = 1 and mydb.games.game_id = """
                db.cursor.execute(query + str(game_id))
                myresult = db.cursor.fetchall()
                
                if myresult==[]:
                    yok="Nobody Wanted to Play :("
                    return render_template('game_index.html',yok=yok,username=username,game_ids=game_id,game_name=game_name)

                return render_template('game_index.html',len=len(myresult),data=myresult,username=username,game_ids=game_id,game_name=game_name)
            
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
                        return render_template('game_index.html',len=len(myresult),data=myresult,username=username,game_ids=game_id,game_name=game_name,haveto="You already created request.")

                    

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
                query="""SELECT mydb.users.user_name, mydb.users.user_surname, mydb.users.user_email, mydb.user_want_to_play_games.User_description  FROM mydb.user_want_to_play_games 
                    LEFT JOIN mydb.users ON mydb.user_want_to_play_games.users_user_id = mydb.users.user_id
                    WHERE  mydb.users.user_findingFriend = 1 and mydb.user_want_to_play_games.id_user_want_to_play_games ="""+ str(id_user_want_to_play_games) # USer_id yanlis geliyor sessiondaki id ile aynı degilse patlıyo
                db.cursor.execute(query)
                myresult = db.cursor.fetchone()

                query =""" SELECT mydb.games_request_messages.games_request_messages, mydb.users.user_name, mydb.users.user_surname, mydb.users.user_email  FROM mydb.games_request_messages 
                    LEFT JOIN mydb.users ON mydb.games_request_messages.users_user_id = mydb.users.user_id
                    WHERE mydb.games_request_messages.user_want_to_play_games_id_user_want_to_play_games = """+str(id_user_want_to_play_games)
                db.cursor.execute(query)
                mycomment = db.cursor.fetchall()

                if mycomment ==[]:
                    print("Mycomment is empty")
                    return render_template('game_contact.html',data=myresult,username=username,game_name=game_name,wantid=id_user_want_to_play_games)
                else:
                    print("Mycomment is not empty")
                    return render_template('game_contact.html',data=myresult,lenRequestAnswer=len(mycomment),RequestAnswer=mycomment,username=username,game_name=game_name,wantid=id_user_want_to_play_games)
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



@app.route('/profile', methods=['GET','POST'])
def profile():
    try:
        if 'user' in session:
            username = session['user'] 
            user_id = session['user_id']
            query = "SELECT * FROM mydb.users where mydb.users.user_id= " + str(user_id)
            db.cursor.execute(query)
            myresult = db.cursor.fetchone()
            ff = myresult[6]
            if ff==1:
                ff_send = "Yes"
            else:
                ff_send = "No"

            if request.method =="GET": #return values for button      
                return render_template('profile.html',data=myresult,username=username,ff_send=ff_send)
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
                    #query= " UPDATE mydb.users SET user_name= '" + str(name)+ "', user_surname= '"+ str(surname)+"', user_schoolNumber = "+str(school_number)+", user_email = '"+ str(email) +"', user_password = "+ str(hash_password) +" WHERE (user_id = "+str(user_id)+") "

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
        else:
            return redirect(url_for("login",haveto="You have to sign in"))
    except:
        print("Profil Sayfa hatası")



@app.route('/profile', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
    return redirect(url_for('sport_index'))

@app.route('/login', methods=['GET','POST'])
def login():
    try:
        if request.method == "POST": 
            session.permanent = True
            if request.form.get("login-button"):
                user_email = request.form["username"] #take username from website textbox
                user_password = request.form["password"].encode('utf-8') #take password from website textbox
                query = "SELECT * FROM mydb.users WHERE user_email =\"" + user_email + "\""
                print(query)
                db.cursor.execute(query)
                Logincheck = db.cursor.fetchone()
                if Logincheck:
                    #if Logincheck[5] == user_password: # check password
                    if bcrypt.hashpw(user_password,Logincheck[5].encode('utf-8') ) == Logincheck[5].encode('utf-8'):
                        session["user"] = Logincheck[1]
                        session["user_id"] = Logincheck[0]
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
                print(str(hash_password))
                query = "SELECT * FROM mydb.users WHERE user_email =\"" + newUser_email + "\""
                db.cursor.execute(query)
                check_email= db.cursor.fetchone()
                print(check_email)
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


if __name__ == '__main__':
    app.run(debug=True)
