import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123456",
  database="wehelp_week6"
)
mycursor = mydb.cursor()