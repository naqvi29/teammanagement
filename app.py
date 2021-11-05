import os
from flask import Flask, flash,session
from flask import jsonify, render_template, request, redirect, url_for, session, jsonify, send_from_directory
from flaskext.mysql import MySQL
from werkzeug.utils import secure_filename
import datetime
import json
from pymysql import cursors
from datetime import datetime,timedelta
from os.path import join, dirname, realpath
from PIL import Image
import random
import string
from flask_socketio import SocketIO, join_room, leave_room,emit


app = Flask(__name__)

# USER IMAGES UPLOAD FOLDER
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/images')
UPLOAD_FOLDER2 = join(dirname(realpath(__file__)), 'static/images/blog')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER2'] = UPLOAD_FOLDER2

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# MYSQL CONFIG
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = ""
app.config["MYSQL_DATABASE_DB"] = "familjehem"
app.config["MYSQL_DATABASE_HOST"] = "localhost"
app.config["MYSQL_DATABASE_PORT"] = 3307
mysql = MySQL(app)

def id_generator(size=8, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

# configure secret key for session
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

# configure socketio 
socketio = SocketIO(app)

@app.route('/')
def admin():
    return render_template("index.html")
# users list 
@app.route('/users-list')
def users_list():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor = conn.cursor(cursors.DictCursor)
    cursor.execute(''' select * from user; ''')
    user_data = cursor.fetchall()    
    cursor.close()
    conn.close()
    return render_template("users-list.html",user_data=user_data)
# add users  
@app.route('/users-add')
def users_add():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor = conn.cursor(cursors.DictCursor)
    cursor.execute(''' select * from user; ''')
    user_data = cursor.fetchall()    
    cursor.close()
    conn.close()
    return render_template("users-list.html",user_data=user_data)
# delete users  
@app.route('/users-delete')
def users_delete():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor = conn.cursor(cursors.DictCursor)
    cursor.execute(''' select * from user; ''')
    user_data = cursor.fetchall()    
    cursor.close()
    conn.close()
    return render_template("users-list.html",user_data=user_data)
# update users  
@app.route('/users-update')
def users_update():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor = conn.cursor(cursors.DictCursor)
    cursor.execute(''' select * from user; ''')
    user_data = cursor.fetchall()    
    cursor.close()
    conn.close()
    return render_template("users-list.html",user_data=user_data)

# assignments list 
@app.route('/assignments-list')
def assignments_list():
    return render_template("assignments-list.html")

# schedules list     
@app.route('/schedules-list')
def schedules_list():
    return render_template("schedules-list.html")

# blogs list 
@app.route('/blogs-list')
def blogs_list():
    return render_template("blogs-list.html")


@app.route('/login', methods=["GET","POST"])
def loginn():
    if session.get("sessionusername"):
        return redirect(url_for("home"))
    else:
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            print(username,password)
            conn = mysql.connect()
            cur = conn.cursor()
            cur.execute(" select * from user where user_name=%s;",[username])
            data = cur.fetchone()
            cur.close()
            conn.close()
            if data != None:
                if data[3] == password:
                    session["sessionusername"] = data[2]
                    session["user_id"] = data[0]
                    return redirect(url_for("home"))
                
                else:
                    session["error"] = "password doesn't match."
                    return redirect(url_for("loginn"))
            else:
                session["error"] = "user not exist."
                error = ""
                if session.get("error"):
                    error = session.get("error")                
                return redirect(url_for("loginn"))

           
        else:
            message = ""
            if session.get("message"):
                message = session.get("message")
                session.pop("message", None)

            error = ""
            if session.get("error"):
                error = session.get("error")
                session.pop("error", None)
            return render_template("login.html", error=error)

@app.route("/logout",methods=["GET","POST"])
def logout():
    session.pop("sessionusername", None)
    return redirect(url_for("loginn"))


################################################ MOBILE API'S START ##########################################################

# ************ FOR SIGNIN ************
@app.route("/signin-api", methods=["POST", "GET"])
def signin_api():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            username = data["username"]
            password = data["password"]
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('''select sno, name, user_name, password, role, img from 
            user where user_name=%s and password=%s;''', [username,password])
            user_data = cursor.fetchone()
            print(user_data)
            cursor.close()
            conn.close()
            if user_data is not None:
                password = user_data[3]
                if password == password:
                    return jsonify({"success":True,"iduser": user_data[0], "name": user_data[1], "user_name":user_data[2], "role": user_data[4], "img": user_data[-1]})
                else:
                    return jsonify({"success": False, "error": "Invalid Credentials"})
            else:
                return jsonify({"success": False, "error": "Invalid Credentials or user doesn't exist."})
        else:
            return jsonify({"success": False, "error": "Invalid request not json format."})
    else:
        return jsonify({"success": False, "error": "Invalid request"})




# ************ FOR SIGNUP ************ BCDE
@app.route("/signup-api/", methods=["POST", "GET"])
def signup_api():
    try:
        if request.method == "POST": 
            name = request.form.get("name")
            username = request.form.get("username")           
            password = request.form.get("password")
            role = request.form.get("role")
            banner_img = request.files["bannerimg"]
            assign_users = None
            if request.form.get("assign_users"):
                assign_users = request.form.get("assign_users")
            # userc
            language = None
            sports = None
            videoname = None
            # userd 
            no_of_rooms = None
            dob = None
            work = None
            interest = None
            # usere 
            about = None
            security = None
            illness = None
            family_speak = None
            other_towns = None

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('''select sno,user_name from user where user_name=%s;''', [username])
            data_user = cursor.fetchone()
            cursor.close()
            conn.close()
            if data_user is None:
                if banner_img.filename != "":
                    filename1 = secure_filename(banner_img.filename)
                    # filename1 = str((datetime.now() + timedelta(hours=5)).strftime("%Y-%m-%d-%H:%M")) + "_" + filename1
                    banner_img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1)) 
                    if role == 'USER B':
                        conn = mysql.connect()
                        cursor = conn.cursor()
                        cursor.execute('''Insert into user (name, user_name, password, role,img,assign_users,language,sports,videoname,no_of_rooms,dob,work,interest,about,security,illness,family_speak,other_towns) values (%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s);''', [name, username, password,role,filename1, assign_users,language,sports,videoname,no_of_rooms,dob,work,interest,about,security,illness,family_speak,other_towns])
                        conn.commit()      
                        cursor.close()
                        conn.close()
                        return jsonify({ "success": True})
                    elif role == 'USER C':
                        language = request.form.get("language")
                        sports = request.form.get("sports")
                        videoname = request.form.get("videoname")
                        conn = mysql.connect()
                        cursor = conn.cursor()
                        cursor.execute('''Insert into user (name, user_name, password, role,img,assign_users,language,sports,videoname,no_of_rooms,work,interest,about,security,illness,family_speak,other_towns) values (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s);''', [name, username, password,role,filename1, assign_users,language,sports,videoname,no_of_rooms,work,interest,about,security,illness,family_speak,other_towns])
                        conn.commit()      
                        cursor.close()
                        conn.close()
                        return jsonify({ "success": True})
                    elif role == 'USER D':
                        no_of_rooms = request.form.get("no_of_rooms")
                        dob = request.form.get("dob")
                        work = request.form.get("work")
                        language = request.form.get("language")
                        interest = request.form.get("interest")
                        conn = mysql.connect()
                        cursor = conn.cursor()
                        cursor.execute('''Insert into user (name, user_name, password, role,img,assign_users,no_of_rooms,dob,work,language,interest) values (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s);''', [name, username, password,role,filename1, assign_users,no_of_rooms,dob,work,language,interest])
                        conn.commit()      
                        cursor.close()
                        conn.close()
                        return jsonify({ "success": True})
                    elif role == 'USER E':
                        about = request.form.get("about")
                        security = request.form.get("security")
                        language = request.form.get("language")
                        dob = request.form.get("dob")
                        illness = request.form.get("illness")
                        family_speak = request.form.get("family_speak")
                        other_towns = request.form.get("other_towns")
                        conn = mysql.connect()
                        cursor = conn.cursor()
                        cursor.execute('''Insert into user (name, user_name, password, role,img,assign_users,about,security,language,dob,illness,family_speak,other_towns) values (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s,%s, %s);''', [name, username, password,role,filename1, assign_users,about,security,language,dob,illness,family_speak,other_towns])
                        conn.commit()      
                        cursor.close()
                        conn.close()
                        return jsonify({ "success": True})
                
            else:
                return jsonify({"success": False, "error": "User already exist with this username."})
        else:
            return jsonify({"success": False, "error": "Invalid request not json format"})
    except Exception as e:
        return jsonify({"status": str(e)})

# ************ FOR USERS LIST ************
@app.route("/users-list-api", methods=["POST", "GET"])
def users_list_api():
   
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(''' select * from user; ''')
    data_user = cursor.fetchall()
    print(data_user)
    cursor.close()
    conn.close()
    
    return jsonify({"success": True, "user":data_user})

# ************ FOR SEARCHING USERS ************
@app.route("/search-users-api/<keyword>", methods=["POST", "GET"])
def search_users_api(keyword):
   if request.method == "GET":
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor = conn.cursor(cursors.DictCursor)
        # cursor.execute(''' select * from user where name LIKE '%s'; ''',[q])
        cursor.execute(''' select * from user where name LIKE %s; ''','%'+keyword+'%')
        data_user = cursor.fetchall()
        print(data_user)
        cursor.close()
        conn.close()
        if not data_user:            
            return jsonify({"success":False, "error":"No match found"})
        else: 
            return jsonify({"success": True, "user":data_user})

# ************ FOR SEARCHING SCHEDULE ************
@app.route("/search-schedule-api/<keyword>", methods=["POST", "GET"])
def search_schedule_api(keyword):
   if request.method == "GET":
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(''' select * from schadule where title LIKE %s; ''','%'+keyword+'%')
        data_schedule = cursor.fetchall()
        print(data_schedule)
        cursor.close()
        conn.close()
        if not data_schedule:            
            return jsonify({"success":False, "error":"No match found"})
        else: 
            return jsonify({"success": True, "user":data_schedule})

# ************ FOR SEARCHING ASSIGNMENT ************
@app.route("/search-assignment-api/<keyword>", methods=["POST", "GET"])
def search_assignment_api(keyword):
   if request.method == "GET":
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(''' select * from assignment where title LIKE %s; ''','%'+keyword+'%')
        data_assignment = cursor.fetchall()
        print(data_assignment)
        cursor.close()
        conn.close()
        if not data_assignment:            
            return jsonify({"success":False, "error":"No match found"})
        else: 
            return jsonify({"success": True, "user":data_assignment})


# ************ FOR USERS2 LIST ************ DICTIONARY
@app.route("/users-list2-api", methods=["POST", "GET"])
def users_list2_api():
   
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor = conn.cursor(cursors.DictCursor)
    cursor.execute(''' select * from user; ''')
    product_data = cursor.fetchall()
 
    
    cursor.close()
    conn.close()
    return jsonify({"success": True, "data":product_data})


# ************ FOR DELETE USERS ************
@app.route("/users-delete-api", methods=["POST", "GET"])
def users_delete_api():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            sno = data["sno"] 
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(''' delete from user where sno=%s; ''',[sno])
           
            conn.commit()      
            cursor.close()
            conn.close()
            return jsonify({"success": True, "Success": "user has Been Deleted "})
        else:
            return jsonify({"success": False, "error": "user not exist"})
    else:
        return jsonify({"success": False, "error": "Invalid request not json format"})
   


# ************ FOR EDIT USERS ************
@app.route("/users-edit-api", methods=["POST", "GET"])
def users_edit_api():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            sno = data["sno"] 
            name = data["name"]
            username = data["username"]               
            password = data["password"] 
            role = data["role"]                         
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('''update  user set name=%s,user_name=%s, password=%s,role=%s where sno=%s;''', [name,username, password,role,sno])
            conn.commit()      
            cursor.close()
            conn.close()
            return jsonify({ "success": True})
            
        else:
            return jsonify({"success": False, "error": "Invalid request not json format"})
    else:
            return jsonify({"success": False, "error": "Invalid request not json format"})

# ************ FOR ADDING SCHEDULE ************
@app.route("/schedule-api", methods=["POST", "GET"])
def schadule():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            title = data["title"] 
            user_id = data["user_id"] 
            user_name = data["user_name"]
            date = data["date"]
            time = data["time"]
            des = data["des"]
            
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('''Insert into schadule (user_id,user_name,title,time,date,des) values (%s,%s,%s,%s,%s,%s);''', [user_id,user_name,title,time,date, des])
            conn.commit()      
            cursor.close()
            conn.close()
            return jsonify({ "success": True})
            
        else:
            return jsonify({"success": False, "error": "Invalid request not json format"})
    else:
            return jsonify({"success": False, "error": "Invalid request not json format"})


# ************ FOR SCHEDULE LIST ************
@app.route("/schedule-list-api")
def schedule_list_api():
    conn = mysql.connect()
    cursor = conn.cursor()
    
    cursor.execute(''' SELECT sno,user_id,user_name,title,DATE_FORMAT(NOW(), '%Y-%m-%d') as "date", TIME_FORMAT(time, "%H %i %p") as "time",(SELECT role FROM user WHERE user.sno = schadule.user_id) as "role", des FROM schadule;''')
    schadule_data = cursor.fetchall()
    print(schadule_data)
   
    cursor.close()
    conn.close()
    return jsonify({ "success": True, "schadule_data":schadule_data}) 

# ************ FOR SCHEDULE LIST ************DICTIONARY
@app.route("/schedule-list2-api")
def schedule_list2_api():
    conn = mysql.connect()
    cursor = conn.cursor(cursors.DictCursor)
    
    cursor.execute(''' SELECT sno,user_id,user_name,title,DATE_FORMAT(NOW(), '%Y-%m-%d') as "date", TIME_FORMAT(time, "%H %i %p") as "time",(SELECT role FROM user WHERE user.sno = schadule.user_id) as "role", des FROM schadule;''')
    schadule_data = cursor.fetchall()
    print(schadule_data)
   
    cursor.close()
    conn.close()
    return jsonify({ "success": True, "schadule_data":schadule_data})         
    

# ************ FOR EDIT SCHEDULE ************
@app.route("/schedule-edit-api", methods=["POST", "GET"])
def schedule_edit_api():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            title = data["title"] 
            user_id = data["user_id"] 
            user_name = data["user_name"]
            date = data["date"]
            time = data["time"]
            des = data["des"]              
            sno = data["sno"]
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('''update  schadule set title=%s,user_id=%s,user_name=%s,date=%s,time=%s, des=%s where sno=%s;''', [title,user_id,user_name,date,time, des,sno])
            conn.commit()      
            cursor.close()
            conn.close()
            return jsonify({ "success": True})
            
        else:
            return jsonify({"success": False, "error": "Invalid request not json format"})
    else:
            return jsonify({"success": False, "error": "Invalid request not json format"})



# ************ FOR DELETING SCHEDULE ************
@app.route("/schedule-delete-api", methods=["POST", "GET"])
def schedule_delete_api():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            sno = data["sno"] 
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(''' delete from schadule where sno=%s; ''',[sno])
           
            conn.commit()      
            cursor.close()
            conn.close()
            return jsonify({"success": True, "Success": "user has Been Deleted "})
        else:
            return jsonify({"success": False, "error": "user not exist"})
    else:
        return jsonify({"success": False, "error": "Invalid request not json format"})



# ************ FOR ADDING ASSIGNMENT ************
@app.route("/assignment-api", methods=["POST", "GET"])
def assignment_api():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            title = data["title"] 
            user_id = data["user_id"] 
            user_name = data["user_name"]
            date = data["date"]
            time = data["time"]
            des = data["des"]
            des = data["des"]               
            
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('''Insert into assignment (title,user_id,user_name,date,time, des) values (%s, %s,%s,%s,%s,%s);''', [title,user_id,user_name,date,time, des])
            conn.commit()      
            cursor.close()
            conn.close()
            return jsonify({ "success": True})
            
        else:
            return jsonify({"success": False, "error": "Invalid request not json format"})
    else:
            return jsonify({"success": False, "error": "Invalid request not json format"})



# ************ FOR ASSIGNMENT LIST ************
@app.route("/assignment-list-api")
def assignment_list_api():
    conn = mysql.connect()
    cursor = conn.cursor()
    
    cursor.execute(''' SELECT sno,user_id,user_name,title,DATE_FORMAT(NOW(), '%Y-%m-%d') as "date", TIME_FORMAT(time, "%H %i %p") as "time",(SELECT role FROM user WHERE user.sno = assignment.user_id) as "role",des FROM assignment;''')
    schadule_data = cursor.fetchall()
    print(schadule_data)
   
    cursor.close()
    conn.close()
    return jsonify({ "success": True, "schadule_data":schadule_data})

# ************ FOR ASSIGNMENT LIST ************DICTIONARY
@app.route("/assignment-list2-api")
def assignment_list2_api():
    conn = mysql.connect()
    cursor = conn.cursor(cursors.DictCursor)
    
    cursor.execute(''' SELECT sno,user_id,user_name,title,DATE_FORMAT(NOW(), '%Y-%m-%d') as "date", TIME_FORMAT(time, "%H %i %p") as "time",(SELECT role FROM user WHERE user.sno = assignment.user_id) as "role",des FROM assignment;''')
    schadule_data = cursor.fetchall()
    print(schadule_data)
   
    cursor.close()
    conn.close()
    return jsonify({ "success": True, "schadule_data":schadule_data})




# ************ FOR EDIT ASSIGNMENT ************
@app.route("/assigment-edit-api", methods=["POST", "GET"])
def assigment_edit_api():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            title = data["title"] 
            user_id = data["user_id"] 
            user_name = data["user_name"]
            date = data["date"]
            time = data["time"]
            des = data["des"]              
            sno = data["sno"]
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('''update  assignment set title=%s,user_id=%s,user_name=%s,date=%s,time=%s, des=%s where sno=%s;''', [title,user_id,user_name,date,time, des,sno])
            conn.commit()      
            cursor.close()
            conn.close()
            return jsonify({ "success": True})
            
        else:
            return jsonify({"success": False, "error": "Invalid request not json format"})
    else:
            return jsonify({"success": False, "error": "Invalid request not json format"})


# ************ FOR DELETING ASSIGNMENT ************
@app.route("/assigment-delete-api", methods=["POST", "GET"])
def assignment_delete_api():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            sno = data["sno"] 
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(''' delete from assignment where sno=%s; ''',[sno])
           
            conn.commit()      
            cursor.close()
            conn.close()
            return jsonify({"success": True, "Success": "user has Been Deleted "})
        else:
            return jsonify({"success": False, "error": "user not exist"})
    else:
        return jsonify({"success": False, "error": "Invalid request not json format"})

# ************ FOR BLOG LIST ************
@app.route("/blog-list-api")
def blog_list_api():
    conn = mysql.connect()
    cursor = conn.cursor(cursors.DictCursor)
    
    cursor.execute(''' SELECT sno,user_id,user_name,blog_pic,title,des,DATE_FORMAT(NOW(), '%Y-%m-%d') as "date", TIME_FORMAT(time, "%H %i %p") as "time",(SELECT role FROM user WHERE user.sno = blog.user_id) as "role" FROM blog;''')
    blog_data = cursor.fetchall()
    print(blog_data)
   
    cursor.close()
    conn.close()
    return jsonify({ "success": True, "blog_data":blog_data})

# ************ FOR ADDING BLOG ************
@app.route("/blog-api", methods=["POST", "GET"])
def blog_api():
    if request.method == "POST":
            user_id = request.form.get('user_id') 
            user_name = request.form.get("user_name")
            date = request.form.get('date')
            time = request.form.get('time')
            des = request.form.get('des')            
            blog_pic = request.files.get('blog_pic')
            title = request.form.get('title')

            if not user_id or not user_name or not des or not title:
                return jsonify({"success": False, "error": "Oops, Something is missing"})

            if blog_pic and allowed_file(blog_pic.filename):
                    filename = secure_filename(blog_pic.filename)
                    blog_pic.save(
                        os.path.join(app.config['UPLOAD_FOLDER2'], filename))
                    # compress image
                    # newimage = Image.open(os.path.join(app.config['UPLOAD_FOLDER2'], str(filename)))
                    # newimage.thumbnail((400, 400))
                    # newimage.save(os.path.join(UPLOAD_FOLDER2, str(filename)), quality=95)
                    # note pillow not installed on server thats why compress code is commented 
            else:
                return jsonify({
                    "success": False,
                    "error": "File not found or incorrect format"
                })
                          
            
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('''Insert into blog (user_id,user_name,blog_pic,title,des,date,time) values (%s, %s,%s,%s,%s,%s,%s);''', [user_id,user_name,filename,title,des,date,time])
            conn.commit()      
            cursor.close()
            conn.close()
            return jsonify({ "success": True ,"msg":"Blog Added!"})
            
    else:
            return jsonify({"success": False, "error": "Invalid request not json format"})

# ************ FOR EDIT BLOG ************
@app.route("/blog-edit-api/<sno>", methods=["POST", "GET"])
def blog_edit_api(sno):
    if request.method == "POST":
            user_id = request.form.get('user_id') 
            user_name = request.form.get("user_name")
            date = request.form.get('date')
            time = request.form.get('time')
            title = request.form.get('title')
            des = request.form.get('des')
            if request.files.get("blog_pic"):            
                blog_pic = request.files.get('blog_pic')
            # checks
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(''' SELECT des from blog where sno=%s;''',[sno])
            blog_data = cursor.fetchall()
            if not blog_data:
                return jsonify({"success":False, "error":"blog not exist"})
            if not user_id or not user_name or not des or not title:
                return jsonify({"success": False, "error": "Oops, Something is missing"})

            if request.files.get('blog_pic'):
                if allowed_file(blog_pic.filename):
                    filename = secure_filename(blog_pic.filename)
                    blog_pic.save(
                        os.path.join(app.config['UPLOAD_FOLDER2'], filename))
                    # compress image
                    # newimage = Image.open(os.path.join(app.config['UPLOAD_FOLDER2'], str(filename)))
                    # newimage.thumbnail((400, 400))
                    # newimage.save(os.path.join(UPLOAD_FOLDER2, str(filename)), quality=95)
                    # note pillow not installed on server thats why compress code is commented 
                else:
                    return jsonify({
                        "success": False,
                        "error": "Incorrect Image format."
                    })
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute('''update blog set user_id=%s,user_name=%s,blog_pic=%s,des=%s,date=%s,time=%s,title=%s where sno=%s;''', [user_id,user_name,filename,des,date,time,title,sno])
                conn.commit()      
                cursor.close()
                conn.close()
            else:
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute('''update blog set user_id=%s,user_name=%s,des=%s,date=%s,time=%s,title=%s where sno=%s;''', [user_id,user_name,des,date,time,title,sno])
                conn.commit()      
                cursor.close()
                conn.close()

            return jsonify({ "success": True, "msg":"Blog updated"})
            
    else:
            return jsonify({"success": False, "error": "Invalid request"})

# ************ FOR DELETING BLOG ************
@app.route("/blog-delete-api", methods=["POST", "GET"])
def blog_delete_api():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            sno = data["sno"] 
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(''' SELECT des from blog where sno=%s;''',[sno])
            blog_data = cursor.fetchall()
            if not blog_data:
                return jsonify({"success":False, "error":"blog not exist"})
            cursor = conn.cursor()
            cursor.execute(''' delete from blog where sno=%s; ''',[sno])
           
            conn.commit()      
            cursor.close()
            conn.close()
            return jsonify({"success": True, "Success": "Blog has Been Deleted "})
        else:
            return jsonify({"success": False, "error": "user not exist"})
    else:
        return jsonify({"success": False, "error": "Invalid request"})

# ************************************* CHATING START ***********************************************

@app.route("/chat-api", methods=["GET", "POST"])
def chatapi():
    try:
        if request.method == "POST":
            return redirect("/chat")
        else:
            # user1 the one who wants to start a chat 
            user1name = ""
            if request.args.get("user1name"):
                user1name = request.args.get("user1name")
            user1id = "NULL"
            if request.args.get("user1id"):
                user1id = request.args.get("user1id")
            # user2 the one with whom he wants to chat 
            user2id = "NULL"
            if request.args.get("user2id"):
                user2id = request.args.get('user2id')
            # usertype is type of the one who wants to chat
            if request.args.get("userType"):
                userType = request.args.get("userType")
            # if userA wants to start a chat with userB
            if user2id != "NULL" and userType == "A":
                conn = mysql.connect()
                cursor = conn.cursor()                
                cursor.execute(''' SELECT * from chatting where (user1id=%s AND user2id=%s) or (user1id =%s AND user2id=%s);''',[user1id,user2id,user2id,user1id])
                chatdata = cursor.fetchone()
                print(chatdata)
                cursor.close()
                cursor = conn.cursor(cursors.DictCursor) 
                cursor.execute(''' SELECT * from user where sno=%s;''',[user2id])
                user2data = cursor.fetchone()
                print(user2data)
                cursor.close()
                if chatdata == None:
                    roomname = id_generator()
                    lastmessagecount = '0'
                    lastmessagetime = str(datetime.now())
                    messages = []
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    cursor.execute('''Insert into chatting (user1id,user1name,user2id,user2name,lastmessagecount,roomname,lastmessagetime,messages) values (%s,%s,%s,%s,%s,%s,%s,%s);''', [user1id,user1name,user2id,user2data['name'],lastmessagecount,roomname,lastmessagetime,messages])
                    conn.commit()      
                    cursor.close()
                    conn.close()

            # if userB wants to start a chat with userA 
            elif user1id != "NULL" and userType == "B":
                conn = mysql.connect()
                cursor = conn.cursor()                
                cursor.execute(''' SELECT * from chatting where (user1id=%s AND user2id=%s) or (user1id =%s AND user2id=%s);''',[user1id,user2id,user2id,user1id])
                chatdata = cursor.fetchone()
                print(chatdata)
                cursor.close()
                cursor = conn.cursor(cursors.DictCursor) 
                cursor.execute(''' SELECT * from user where sno=%s;''',[user1id])
                user1data = cursor.fetchone()
                print(user1data)
                cursor.close()
                cursor = conn.cursor(cursors.DictCursor) 
                cursor.execute(''' SELECT * from user where sno=%s;''',[user2id])
                user2data = cursor.fetchone()
                print(user2data)
                cursor.close()
                if chatdata == None:
                    roomname = id_generator()
                    lastmessagecount = '0'
                    lastmessagetime = str(datetime.now())
                    messages = []
                    cursor = conn.cursor()
                    cursor.execute('''Insert into chatting (user1id,user1name,user2id,user2name,lastmessagecount,roomname,lastmessagetime,messages) values (%s,%s,%s,%s,%s,%s,%s,%s);''', [user1id,user1data['name'],user2id,user2data['name'],lastmessagecount,roomname,lastmessagetime,messages])
                    conn.commit()      
                    cursor.close()
                    conn.close()
            # show all chats for just oneid 
            # jiska inbox kholna hai uski id or user type deni hai bs 
            if userType == "B":                
                conn = mysql.connect()
                cursor = conn.cursor(cursors.DictCursor)                
                cursor.execute(''' SELECT * from chatting where (user1id=%s)or(user2id=%s);''',[user2id,user2id])
                data = cursor.fetchall()
                print(data)
                cursor.close()
                conn.close()
            elif userType == "A":
                conn = mysql.connect()
                cursor = conn.cursor(cursors.DictCursor)                
                cursor.execute(''' SELECT * from chatting where user1id=%s;''',[user1id])
                data = cursor.fetchall()
                print(data)
                cursor.close()
                conn.close()
            elif userType == "C":
                conn = mysql.connect()
                cursor = conn.cursor(cursors.DictCursor)                
                cursor.execute(''' SELECT * from chatting where user2id=%s;''',[user1id])
                data = cursor.fetchall()
                print(data)
                cursor.close()
                conn.close()
            elif userType == "D":
                conn = mysql.connect()
                cursor = conn.cursor(cursors.DictCursor)                
                cursor.execute(''' SELECT * from chatting where user2id=%s;''',[user1id])
                data = cursor.fetchall()
                print(data)
                cursor.close()
                conn.close()
            elif userType == "E":
                conn = mysql.connect()
                cursor = conn.cursor(cursors.DictCursor)                
                cursor.execute(''' SELECT * from chatting where user2id=%s;''',[user1id])
                data = cursor.fetchall()
                print(data)
                cursor.close()
                conn.close()
            
            # note: sirf user a or b chat start kar sakty hain sab users se or user c.d.e sirf apna inbox access kar sakty hain 

            newdata = []
            for chats in data:
                chats.update({"sno": str(chats["sno"]), "user2id": str(chats["user2id"]), "user1id": str(chats["user1id"])})
                newdata.append(chats)
            return jsonify({"data":newdata, "username":user1name, "userid":user1id, "user2id":user2id,
            })
    except Exception as e:
        return jsonify({"status": str(e)})

@app.route("/getmessages", methods=["POST"]) #not using 
def getmessages():
    try:
        if request.is_json:
            data = request.get_json()
            user1id = data["user1id"]
            user2id = data["user2id"]
            conn = mysql.connect()
            cur = conn.cursor()
            cur.execute("select messages from chatting where user1id = %s and user2id = %s", [user1id,user2id])
            messages = cur.fetchone()
            cur.close()
            conn.close()
        if messages[0] != None:
            # messages = str(messages[0]).replace("'", '"')
            # messages = str(messages).split("&&")
            messagedata = []
            for curmessg in messages:
                mess = json.loads(curmessg)
                messagedata.append(mess)

            messages = messagedata
            print(messages)
            print(type(messages))
        else:
            messages = []

        return jsonify({"success": True, "messages": messages})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@socketio.on('app event') #updated from testsocket
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received app event: ' + str(json))
    # jisko msg kar raha hai
    username = ""
    if "user_name" in json:
        username = json["user_name"]
    # jo msg kar raha hai 
    curuser = json["userid"]
    print(curuser)
    roomname = ""
    if "roomname" in json:
        roomname = json["roomname"]
        join_room(roomname)

    print(json["message"])
    if json["message"] != "connected":
        lastmessagetime = datetime.now()
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('''update  chatting set lastmessagetime=%s where roomname=%s;''', [lastmessagetime,roomname])
        conn.commit()      
        cursor.close()

        cursor = conn.cursor()
        cursor.execute(" select messages from chatting where roomname=%s;",[roomname])
        olddata = cursor.fetchone()
        print(olddata[0])
        # if  olddata[0] is not None:
        if  olddata[0] != "":
            print("not none yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
        
            messages = json.loads(str(olddata[0]))
            cursor.close()
            
            print(messages)
            newmessage = {"status": curuser, "message": json["message"], "type": "text",
                                                "timeStamp": datetime.now().time().strftime("%H:%M:%S:%f"),
                                                "time": datetime.now().time().strftime("%H:%M")}
            print (newmessage)
            updated = str(messages)+str(newmessage)
            print ("updated",updated)
            
            
            messagejson = json.dumps(updated)
            cursor = conn.cursor()
            cursor.execute('''update chatting set messages=%s where roomname=%s;''', [messagejson,roomname])
            conn.commit()  
            cursor.close()
        else:
            print("none  xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            newmessage = {"status": curuser, "message": json["message"], "type": "text",
                                                "timeStamp": datetime.now().time().strftime("%H:%M:%S:%f"),
                                                "time": datetime.now().time().strftime("%H:%M")}
            messagejson = json.dumps(newmessage)
            cursor = conn.cursor()
            cursor.execute('''update chatting set messages=%s where roomname=%s;''', [messagejson,roomname])
            conn.commit()  
            cursor.close()

    socketio.emit('my response', json, room=roomname, callback=json)
    

@app.route("/testsocket",methods=['POST']) #tested 100% works
def testsocket(): #only for testing
    try:
        if request.is_json:
            data = request.get_json()
            # jisko msg kar raha hai 
            username = ""
            if "user_name" in request.get_json():
                username = data["user_name"]
            # jo msg kar raha hai 
            curuser = data["userid"]
            print(curuser)
            roomname = ""
            if "roomname" in request.get_json():
                roomname = data["roomname"]
            if data["message"] != "connected":
                lastmessagetime = datetime.now()
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute('''update  chatting set lastmessagetime=%s where roomname=%s;''', [lastmessagetime,roomname])
                conn.commit()      
                cursor.close()

                cursor = conn.cursor()
                cursor.execute(" select messages from chatting where roomname=%s;",[roomname])
                olddata = cursor.fetchone()
                print(olddata[0])
                # if  olddata[0] is not None:
                if  olddata[0] != "":
                    print("not none yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
                
                    messages = json.loads(str(olddata[0]))
                    cursor.close()
                    
                    print(messages)
                    newmessage = {"status": curuser, "message": data["message"], "type": "text",
                                                        "timeStamp": datetime.now().time().strftime("%H:%M:%S:%f"),
                                                        "time": datetime.now().time().strftime("%H:%M")}
                    print (newmessage)
                    updated = str(messages)+str(newmessage)
                    print ("updated",updated)
                    
                    
                    messagejson = json.dumps(updated)
                    cursor = conn.cursor()
                    cursor.execute('''update chatting set messages=%s where roomname=%s;''', [messagejson,roomname])
                    conn.commit()  
                    cursor.close()
                    return jsonify({"success":True})
                else:
                    print("none  xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
                    newmessage = {"status": curuser, "message": data["message"], "type": "text",
                                                        "timeStamp": datetime.now().time().strftime("%H:%M:%S:%f"),
                                                        "time": datetime.now().time().strftime("%H:%M")}
                    messagejson = json.dumps(newmessage)
                    cursor = conn.cursor()
                    cursor.execute('''update chatting set messages=%s where roomname=%s;''', [messagejson,roomname])
                    conn.commit()  
                    cursor.close()
                
                    return jsonify({"success":True})

        else:
            return jsonify({"success":False, "error":"invalid json"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


    




if __name__ == "__main__":
    app.run(debug=True)