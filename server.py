from flask import Flask, abort, current_app, render_template, request, session, url_for, redirect, flash
import mysql.connector
from flask_mysqldb import MySQL
from database import Database

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
            return render_template('home.html',len=len(myresult), username=username)
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
                return render_template('sports.html',len=len(myresult),data=myresult,username=username)

        else:
            return redirect(url_for("login",haveto="You have to sign in"))
    except:
        print("Sport Sayfa hatası")

@app.route('/sports/<int:sport_id>', methods=['GET','POST'])
def index(sport_id):
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
                    return render_template('index.html',yok=yok,username=username,sport_ids=sport_id,sport_name=sport_name)
                print("adasd",myresult)
                return render_template('index.html',len=len(myresult),data=myresult,username=username,sport_ids=sport_id,sport_name=sport_name)
            
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
                        return render_template('index.html',len=len(myresult),data=myresult,username=username,sport_ids=sport_id,sport_name=sport_name,haveto="You already created request.")

                    

                return redirect(url_for("sports"))
        else:
            return redirect(url_for("login",haveto="You have to sign in"))
    except:
        print("index hata")


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
                    return render_template('contact.html',data=myresult,username=username,sport_ids=sport_id,sport_name=sport_name,haveto="You already created request.",wantid=id_User_want_to_play_sports)
                else:
                    print("Mycomment is not empty")
                    return render_template('contact.html',data=myresult,lenRequestAnswer=len(mycomment),RequestAnswer=mycomment,username=username,sport_ids=sport_id,sport_name=sport_name,haveto="You already created request.",wantid=id_User_want_to_play_sports)
            else:
                if request.form.get("add_comment"):
                    print("Db ye eklendi")
                    user_description = request.form["email"] #request 
                    query="INSERT INTO mydb.sport_request_messages ( request_messages, user_want_to_play_sports_id_User_want_to_play_sports, users_user_id, sports_sport_id) VALUES (%s,%s,%s, %s)"
                    val = (user_description,id_User_want_to_play_sports,Session_user_id,sport_id)
                    print("Db ye eklendi", query, val)
                    db.cursor.execute(query, val) #added the database
                    db.con.commit()
                    print("Db ye eklendi")
                    return redirect(url_for("contact",sport_id=sport_id,id_User_want_to_play_sports=id_User_want_to_play_sports))
            
        else:
            return redirect(url_for("login",haveto="You have to sign in"))
    except:
        print("contact hata")

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
                    query= " UPDATE mydb.users SET user_name= '" + str(name)+ "', user_surname= '"+ str(surname)+"', user_schoolNumber = "+str(school_number)+", user_email = '"+ str(email) +"' WHERE (user_id = "+str(user_id)+") "
                    db.cursor.execute(query)
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
        else:
            return redirect(url_for("login",haveto="You have to sign in"))
    except:
        print("Sport Sayfa hatası")



@app.route('/login', methods=['GET','POST'])
def login():
    try:
        if request.method == "POST": 
            session.permanent = True
            if request.form.get("login-button"):
                user_email = request.form["username"] #take username from website textbox
                user_password = request.form["password"] #take password from website textbox
                
                query = "SELECT * FROM mydb.users WHERE user_email =\"" + user_email + "\""
                print(query)
                db.cursor.execute(query)
                Logincheck = db.cursor.fetchone()
            
                if Logincheck:
                    
                    if Logincheck[5] == user_password:
                        session["user"] = Logincheck[1]
                        session["user_id"] = Logincheck[0]
                        # return render_template('home.html',len=1,data=[1,2],table_name="Sports",username= session["user"])
                        return redirect(url_for("home_page"))

                    else:
                        print("WRONG PASSWORD")

                else:
                    print("WRONG USERNAME")
                    
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
