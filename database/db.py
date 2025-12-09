import mysql.connector


db = mysql.connector.connect(host ="localhost", 
                            user = "mohammad",
                            password = "facedetect")

mycursor = db.cursor()

mycursor.execute("CREATE DATABASE facedetect")

mycursor.execute("CREATE TABLE detection (id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(255) , time DATETIME , uuid VARCHAR(100)")