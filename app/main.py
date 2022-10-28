from distutils.command.build_clib import build_clib
from distutils.command.upload import upload
from itertools import count
from multiprocessing.sharedctypes import Value
from tkinter import Y
from urllib import response
from urllib.parse import MAX_CACHE_SIZE
from wsgiref.validate import validator
from flask import Flask, Request, redirect, render_template, request, url_for
import os
from numpy import size
from werkzeug.utils import  secure_filename
from flask import json
import pymysql.cursors
import pymysql
from app import memcache,webapp
from pymemcache.client.base import Client
from datetime import datetime
import time
import ttl_cache
from expiringdict import ExpiringDict
from flask import jsonify

from apscheduler.schedulers.background import BackgroundScheduler
import atexit





def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

value ="unknown"
count = 0
countall = 0
maxcapacity=50000000
counthit=0
countmiss=0
filesize=0


conn = pymysql.connect(host='localhost', user='root', password='', db='cloude_dp')
cur = conn.cursor()

UPLOAD_FOLDER = "app/static/img/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

webapp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def displayKey():
           
          
           conn = pymysql.connect(host='localhost', user='root', password='', db='cloude_dp')
           cur = conn.cursor()
           sql_statement = "SELECT keyy FROM uuu"
           cur.execute(sql_statement)
           output = cur.fetchall()
           conn.commit()
           conn.close()
           
           return output
           




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



@webapp.route('/page3.html', methods=["POST"])
def ind():
      
      users =displayKey()
      
      return render_template("page3.html", usr=users)


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

def countmemc():
    countmem=0
    for i in memcache:
      countmem =countmem+1
    print(countmem,' in meme cache')
    return countmem





@webapp.route("/page2.html", methods = ['POST'])
def ind1(): 
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=print_date_time, trigger="interval", seconds=5)
    scheduler.start()
    key = request.form['keyy']
    if key in memcache:
        value = memcache[key]
        n= memcache.get(key)
        global counthit
        counthit= counthit+1
        print(counthit,'hitttttttttt')
        print(memcache)
        atexit.register(lambda: scheduler.shutdown())
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
        print(countmiss,'misssssssssssssssss')
        conn.commit()
        print(value)
        conn.close()
        

    return render_template("page2.html", res=value[0][0], c= count)



# -******************************************page 4***********************************************

@webapp.route("/page4.html", methods = ['POST'])
def getmem():
    listkey= list(memcache.keys())
    delete=memcache.clear()
    return render_template("page4.html",listkey=listkey,delete=delete)


# *************************************************************************************************










    
@webapp.route("/page5.html", methods = ['POST'])
def confmem():
    max = "50M"
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=print_date_time, trigger="interval", seconds=5)
    scheduler.start()
    all=counthit+countmiss
    hitrate= (counthit/all)*100
    missrate=(countmiss/all)*100
    print(hitrate)
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())



       

    return render_template("page5.html",max=max,hitrate=hitrate,missrate=missrate)




