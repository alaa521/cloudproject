from flask import render_template, request
import os
from werkzeug.utils import  secure_filename
import pymysql.cursors
import pymysql
from app import memcache,webapp
import time
from apscheduler.schedulers.background import BackgroundScheduler
import atexit




# Definesion variable
count = 0
maxcapacity=50000000
counthit=0      #hit rate 
countmiss=0     #miss rate


# connaction with Database
conn = pymysql.connect(host='localhost', user='root', password='', db='cloude_dp')
cur = conn.cursor()

#Definesion extension and path folder image
UPLOAD_FOLDER = "app/static/img/"   
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
webapp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#page 5
def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

#page 1
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#page 3 
def displayKey():
    conn = pymysql.connect(host='localhost', user='root', password='', db='cloude_dp')
    cur = conn.cursor()
    sql_statement = "SELECT keyy FROM uuu"
    cur.execute(sql_statement)
    output = cur.fetchall()
    conn.commit()
    conn.close()
    return output
           
def countmemc():
    countmem=0
    for i in memcache:
      countmem =countmem+1
    print(countmem,' in meme cache')
    return countmem




# ****************************** Page Navigation************************
@webapp.route('/')
def main():
    return render_template("index.html")

@webapp.route('/index.html', methods=["GET"])
def page1(): 
    subject= request.args.get('page1')
    return render_template("index.html") 

@webapp.route('/page2.html', methods=["GET"])
def page2(): 
    subject= request.args.get('page2')
    return render_template("page2.html")

@webapp.route('/page3.html', methods=["GET"])
def page3(): 
    subject= request.args.get('page3')
    return render_template("page3.html")

@webapp.route('/page4.html', methods=["GET"])
def page4(): 
    subject= request.args.get('page4')
    return render_template("page4.html") 

@webapp.route('/page5.html', methods=["GET"])
def page5(): 
    subject= request.args.get('page5')
    return render_template("page5.html")    

# ****** ُ***********************End Page Navigation**************************

# *****************page 1 --- Inser image and Update in database ---************************
@webapp.route("/upload", methods = ['GET','POST'])
def addimg():
    conn = pymysql.connect(host='localhost', user='root', password='', db='cloude_dp')
    cur = conn.cursor()
    if request.method == 'GET':
        return render_template("page2.html")

    if request.method == 'POST':
        keyy = request.form.get('keyy')
        file = request.files['image']
        global file_name
        file_name = secure_filename(file.filename)
        print(file_name)
        print(file)
        file.save(os.path.join(UPLOAD_FOLDER ,file_name))

        # search if key in DB update the image , if not insert key and image
        count = cur.execute('select * from uuu where keyy=%s', [keyy])  # prevent SqlInject
        if count==0:
          cur.execute("INSERT INTO uuu (keyy,image) VALUES (%s, %s)", [keyy,file_name])
          sucsess = 'sucsess insert'  
        else:
          cur.execute("UPDATE uuu SET image = %s  WHERE keyy = %s" , [file_name,keyy])
          sucsess = 'sucsess update'
        conn.commit()
        cur.close()
        return render_template('index.html', sucsess=sucsess)
    else:
        sucsess = 'FAILD ADDED '
        return render_template('index.html',sucsess=sucsess)



# *************************page 2 ---Enter Key thats show image ---************************
@webapp.route("/page2.html", methods = ['POST'])
def ind1(): 
    key = request.form['keyy']
    if key in memcache:
        value = memcache[key]
        memcache.get(key)
        global counthit
        counthit= counthit+1
        print(counthit,'hit')
        print(memcache)
        count=1
    else:
        conn = pymysql.connect(host='localhost', user='root', password='', db='cloude_dp')
        cur = conn.cursor()
        sql = "select image from uuu where keyy=%s"
        cur.execute(sql,key)
        value = cur.fetchall()
        memcache[key] = value
        count = 0
        global countmiss
        countmiss=countmiss+1
        print(countmiss,'miss')
        conn.commit()
        print(value)
        conn.close()
    return render_template("page2.html", res=value[0][0], c= count)

# -***********************page 3 --- list of key in DATABASE --- ***************************
@webapp.route('/page3.html', methods=["POST"])
def ind():
      users =displayKey()
      return render_template("page3.html", usr=users)


# -***********************page 4 --- list of key in Memory cach  and delete  --- ***************************
@webapp.route("/page4.html", methods = ['POST'])
def getmem():
    listkey= list(memcache.keys())
    delete=memcache.clear()
    return render_template("page4.html",listkey=listkey,delete=delete)

# ********** *************page5 ---show configration memcach ********************************  
@webapp.route("/page5.html", methods = ['POST'])
def confmem():
    max = "50M"
    #we use BackgroundScheduler() from APScheduler package 
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=print_date_time, trigger="interval", seconds=5)
    scheduler.start()
    all=counthit+countmiss
    hitrate= (counthit/all)*100
    missrate=(countmiss/all)*100
    print(hitrate)
    
    # conn = pymysql.connect(host='localhost', user='root', password='', db='cloude_dp')
    # cur = conn.cursor()
    # cur.execute("UPDATE config SET hitrate = %s,missrate=%s  WHERE max =  " , [hitrate,missrate])
    # conn.commit()
    # conn.close()


    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
    return render_template("page5.html",max=max,hitrate=hitrate,missrate=missrate)




