
import mysql.connector
from django.contrib.auth.models import User
from datetime import datetime
from mysite.shift import Shift
from mysite.air_crew import AirCrew



mydb = mysql.connector.connect(host="localhost", user="root", password = 'a1234567', database = 'flight_manager'
                               ,auth_plugin='mysql_native_password')
from mysite.shift import Shift
class Contact():
    def __init__(self):
        self.personal_num= ""
        self.date = ""
        self.name = ""
        self.content = ""

    def insertcontent(self, personal_num, content):
        air_crew = AirCrew()
        val = (personal_num,content)
        mydb = mysql.connector.connect(host="localhost", user="root", password='a1234567',
                                       database='flight_manager',
                                       auth_plugin='mysql_native_password')
        mycursor = mydb.cursor()
        query = """ insert into contact(personal_num, date, content)
                               VALUES(%s, curdate(),%s)"""
        mycursor.execute(query, val)
        mydb.commit()

    def deleteletter(self,personal_num,date,  content):
        args = (personal_num, date, content,)
        mydb = mysql.connector.connect(host="localhost", user="root", password='a1234567', database='flight_manager',
                                       auth_plugin='mysql_native_password')
        mycursor = mydb.cursor()
        query = """
                delete from flight_manager.contact
                where personal_num = %s and date = %s and content = %s ;

                                        """
        mycursor.execute(query, args)
        mydb.commit()















