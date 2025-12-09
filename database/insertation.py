import mysql.connector
from src.utils.logger import logger
from database.connection import get_connection


logger = logger("insertation")

def insertation(name , time  , uuid):
    db = get_connection()
    mycurser = db.cursur()
    sql = "INSERT INTO detection (name,time,uuid) VALUES (%s ,%s ,%s)"
    val = (name , time , uuid)
    mycurser.excute(sql , val)
    db.commit()
    logger.info("the record inserted ! ") 
    
    
       
