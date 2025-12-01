import _mysql_connector

def get_connection():
    return _mysql_connector.connect(host ="localhost", 
                            user = "mohammad",
                            password = "facedetect",
                            database= 'facedetect')