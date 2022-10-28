from distutils.command.build_clib import build_clib
from distutils.command.upload import upload
from msilib.schema import SelfReg
from ssl import AlertDescription
from typing_extensions import Self
from urllib import response
from wsgiref.validate import validator
from flask import Flask, redirect, render_template, request, url_for

from flask import json
import pymysql.cursors
import pymysql

from pymemcache.client.base import Client
print(66666666666666666666)
client = Client('0.0.0.0',5001)
print(8888888888888888888888)

conn = pymysql.connect(host='localhost', user='root', password='', db='cloude_dp')
cur = conn.cursor()
memcache = {}

UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData
def get():
    key = request.form.get('key')

    if key in memcache:
        value = memcache[key]
        response = app.response_class(
            response=json.dumps(value),
            status=200,
            mimetype='application/json'
        )
    else:
        response = app.response_class(
            response=json.dumps("Unknown key"),
            status=400,
            mimetype='application/json'
        )

    return response

def put():
    key = request.form.get('key')
    value = request.form.get('value')
    memcache[key] = value

    response = app.response_class(
        response=json.dumps("OK"),
        status=200,
        mimetype='application/json'
    )

    return response



def displayKey():
           
           print(66666666666)
           conn = pymysql.connect(host='localhost', user='root', password='', db='cloude_dp')
           cur = conn.cursor()
           sql_statement = "SELECT keyy FROM hhh"
           cur.execute(sql_statement)
           output = cur.fetchall()
           conn.commit()
           conn.close()
           print(output)
           return output
           




@app.route('/')
def main():
    return render_template("index.html")

@app.route('/index.html', methods=["GET"])
def page1(): 
    subject= request.args.get('page1')
    return render_template("index.html") 

@app.route('/page2.html', methods=["GET"])
def page2(): 
    subject= request.args.get('page2')
    return render_template("page2.html")

@app.route('/page3.html', methods=["GET"])
def page3(): 
    subject= request.args.get('page3')
    return render_template("page3.html")


@app.route('/page4.html', methods=["GET"])
def page4(): 
    subject= request.args.get('page4')
    return render_template("page4.html")  


@app.route("/page4.html", methods = ['GET','POST'])
 





@app.route("/page3.html", methods = ['GET','POST'])


def ind():
      
      users =displayKey()
      
      return render_template("page3.html", usr=users)


@app.route("/upload", methods = ['GET','POST'])
def addimg():
    conn = pymysql.connect(host='localhost', user='root', password='', db='cloude_dp')
    cur = conn.cursor()
    if request.method == 'GET':
        return render_template("page2.html")
    if request.method == 'POST':
        keyy = request.form["keyy"]
        file = request.files['image']
        file_name = file.filename or ''
        destination = '/'.join([UPLOAD_FOLDER, file_name])
        file.save(destination)
        convertToBinaryData(file.filename)
        count = cur.execute('select * from hhh where keyy=%s', [keyy])  # prevent SqlInject
        if count==0:
          cur.execute("INSERT INTO hhh (keyy,image) VALUES (%s, %s)", [keyy,file])
          print(4444444)
          sucsess = 'sucsess insert'
        else:
          cur.execute("UPDATE hhh SET image = %s  WHERE keyy = %s" , [file,keyy])
          print(666666)
          sucsess = 'sucsess update'
        conn.commit()
        cur.close()
        return render_template('index.html', sucsess=sucsess)
    else:
        return render_template('index.html')


def convertBinaryToFile(binarydata,filename):
    with open(filename,'wb') as file:
        file.write(binarydata)

@app.route("/page2", methods = ['POST'])
def ind1():
    print(999999900000)
    print(request.method)
    conn = pymysql.connect(host='localhost', user='root', password='', db='cloude_dp')
    cur = conn.cursor()
    print(777777777777777777)
    if request.method == 'POST':
        keyy = request.form["keyy"]
        file = request.files['image']
        print(11111111111111111111111111)
        sql_statement = cur.execute('SELECT image FROM hhh  WHERE keyy=?', [keyy])
        convertBinaryToFile(sql_statement,file)
        output = cur.fetchall()
        conn.commit()
        conn.close()
        print(output)
        return render_template("page2.html")
    else :
      return render_template('page2.html')



