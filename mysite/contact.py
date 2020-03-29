
import mysql.connector
from django.contrib.auth.models import User
from datetime import datetime
from mysite.shift import Shift
from mysite.air_crew import AirCrew



mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319", password = 'c786913f', database = 'heroku_947e29c06a5b4a3',auth_plugin='mysql_native_password')

from mysite.shift import Shift
class Contact():
    def __init__(self):
        self.personal_num= ""
        self.date = ""
        self.name = ""
        self.content = ""

    def insertcontent(self, personal_num, content):
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

        air_crew = AirCrew()
        val = (personal_num,content)
        mycursor = mydb.cursor()
        query = """ insert into contact(personal_num, date, content)
                               VALUES(%s, curdate(),%s)"""
        mycursor.execute(query, val)
        mydb.commit()

    def deleteletter(self,personal_num,date,  content):
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

        args = (personal_num, date, content,)
        mycursor = mydb.cursor()
        query = """
                delete from contact
                where personal_num = %s and date = %s and content = %s ;

                                        """
        mycursor.execute(query, args)
        mydb.commit()















