from flask import Flask,render_template,request
import mysql.connector as mys
import json

app = Flask(__name__,template_folder="pages")

mysqlConnection = mys.connect(host="localhost",user="root",password="root")
cursor = mysqlConnection.cursor()
dbExists = False
cursor.execute("show databases;")
for i in cursor:
	if i[0] == "blogdb":
		dbExists = True
if dbExists:
	cursor.execute("use blogdb;")
else:
	cursor.execute("create database blogdb;")
	cursor.execute("use blogdb;")
	cursor.execute("create table blogs(title varchar(30), content varchar(200));")
	mysqlConnection.commit()

@app.route("/")
def home():
	return render_template("home.html")

@app.route("/create")
def create():
	return render_template("create.html")

@app.route("/api/create",methods=["POST"])
def createblog():
	title = request.json["title"]
	content = request.json["content"]
	cursor.execute(f"insert into blogs values('{title}','{content}');")
	mysqlConnection.commit()
	return "Blog created"

@app.route("/api/getBlogs")
def getblogs():
	cursor.execute("select * from blogs;")
	blogs = []
	for i in cursor:
		blogs.insert(0,{"title":i[0],"content":i[1]})
	return blogs

app.run(host="localhost",port=2255,debug=True)