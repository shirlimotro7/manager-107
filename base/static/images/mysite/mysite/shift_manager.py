

import mysql.connector
from django.contrib.auth.models import User
from datetime import datetime
from mysite.shift import Shift
from mysite.air_crew import AirCrew
from mysite.contact import Contact




mydb = mysql.connector.connect(host="localhost", user="root", password = 'a1234567', database = 'flight_manager',auth_plugin='mysql_native_password')
from mysite.shift import Shift
class ShiftManager():
    def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.personal_num = ""



    def getname(self, username):
        mydb = mysql.connector.connect(host="localhost", user="root", password='a1234567', database='flight_manager',
                                       auth_plugin='mysql_native_password')
        mycursor = mydb.cursor()
        query = """
                 SELECT first_name, last_name FROM flight_manager.auth_user WHERE username= %s 
                """
        mycursor.execute(query, username)
        results = mycursor.fetchall()
        mydb.commit()
        name = []
        for row in results:
            first_name = row[0]
            last_name = row[1]
            name.append(first_name.capitalize())
            name.append(last_name.capitalize())
        return name[0] +' ' + name[1]

    def insertshift(self, date, type, notes):
        val = (date, type, notes,)
        mydb = mysql.connector.connect(host="localhost", user="root", password='a1234567', database='flight_manager',
                                       auth_plugin='mysql_native_password')
        mycursor = mydb.cursor()
        query = """ insert into shifts(flight_date,flight_type, notes)
                            VALUES(%s,%s,%s)"""
        mycursor.execute(query, val)
        mydb.commit()

    def insertgoals(self, azach_num, miluim_num):
        val1 = (azach_num,)
        val2 =  (miluim_num,)
        mydb = mysql.connector.connect(host="localhost", user="root", password='a1234567',
                                       database='flight_manager',
                                       auth_plugin='mysql_native_password')
        mycursor = mydb.cursor()
        query = """ insert into flight_manager.goals(status, goal)
                    VALUES('azach',%s );
                    
                """
        mycursor.execute(query, val1)
        mydb.commit()
        query2 = """
                    insert into flight_manager.goals(status, goal)
                    VALUES('miluim', %s )
                """
        mycursor.execute(query2, val2)
        mydb.commit()

    def getletters(self):
        mydb = mysql.connector.connect(host="localhost", user="root", password='a1234567', database='flight_manager',
                                       auth_plugin='mysql_native_password')
        mycursor = mydb.cursor()
        query = """
                    select * from flight_manager.contact
               """
        mycursor.execute(query)
        results = mycursor.fetchall()
        mydb.commit()
        letters = []
        for row in results:
            contact = Contact()
            air_crew = AirCrew()
            contact.personal_num = str(row[0])
            personal_num = str(row[0]).capitalize()
            contact.date = str(row[1])
            contact.content = str(row[2])
            contact.name = air_crew.getname((personal_num,))
            letters.append(contact)
        return letters




    def unmannedshifts(self):
        mydb = mysql.connector.connect(host="localhost", user="root", password='a1234567', database='flight_manager',
                                       auth_plugin='mysql_native_password')
        mycursor = mydb.cursor()
        query = """
            SELECT flight_manager.shifts.flight_date,  flight_manager.shifts.flight_type,  flight_manager.type_of_shift.crew_role,  flight_manager.type_of_shift.leader
            from flight_manager.shifts join flight_manager.type_of_shift
            on shifts.flight_type = type_of_shift.flight_type 
            left join flight_manager.staffing
            on flight_manager.shifts.flight_date = flight_manager.staffing.flight_date
            and flight_manager.type_of_shift.flight_type = flight_manager.staffing.flight_type
            and (flight_manager.type_of_shift.crew_role = flight_manager.staffing.crew_role
            or flight_manager.type_of_shift.crew_role = 'all')
            and flight_manager.type_of_shift.leader = flight_manager.staffing.leader
            where personal_num is NULL

            
                """
        mycursor.execute(query)
        results = mycursor.fetchall()
        mydb.commit()
        unmenned_shifts = []
        count = 1
        for row in results:
            shift = Shift()
            shift.number = count
            count = count +1
            shift.flight_date = str(row[0])
            shift.flight_type = str(row[1]).capitalize()
            shift.crew_role =str(row[2]).capitalize()
            if str(row[3]) =='1':
                shift.leader = 'Must Be Movil'
            elif str(row[3]) == '0':
                shift.leader = 'Number 2'
            else :
                shift.leader = 'All'
            unmenned_shifts.append(shift)
        return unmenned_shifts


    def goaltracker(self):
        mydb = mysql.connector.connect(host="localhost", user="root", password='a1234567', database='flight_manager',
                                       auth_plugin='mysql_native_password')
        mycursor = mydb.cursor()
        query = """
            select flight_manager.air_crew.personal_number, flight_manager.auth_user.first_name, flight_manager.auth_user.last_name, 
            flight_manager.air_crew.goal, count(flight_manager.staffing.personal_num) As achieved
            from flight_manager.auth_user  join flight_manager.air_crew
            on flight_manager.auth_user.username = flight_manager.air_crew.personal_number
            left join flight_manager.staffing
            on flight_manager.air_crew.personal_number = flight_manager.staffing.personal_num
            group by air_crew.personal_number;
            
            """
        mycursor.execute(query)
        results = mycursor.fetchall()
        mydb.commit()
        air_goals = []
        for row in results:
            air_crew = AirCrew()
            air_crew.personal_num = str(row[0])
            air_crew.first_name = str(row[1]).capitalize()
            air_crew.last_name = str(row[2]).capitalize()
            air_crew.goal = str(row[3])
            air_crew.achieved = str(row[4])
            air_goals.append(air_crew)
        return air_goals

    def staffnumber(self):
        mydb = mysql.connector.connect(host="localhost", user="root", password='a1234567', database='flight_manager',
                                       auth_plugin='mysql_native_password')
        mycursor = mydb.cursor()
        query = """
            select count(personal_number) As num_of_people
            from flight_manager.air_crew
                """
        mycursor.execute(query)
        results = mycursor.fetchall()
        mydb.commit()
        for row in results:
            num_of_crew = str(row[0])
        return num_of_crew

    def totalgoal(self):
        mydb = mysql.connector.connect(host="localhost", user="root", password='a1234567', database='flight_manager',
                                       auth_plugin='mysql_native_password')
        mycursor = mydb.cursor()
        query = """
                    select sum(goal) 
                    from flight_manager.air_crew
                        """
        mycursor.execute(query)
        results = mycursor.fetchall()
        mydb.commit()
        for row in results:
            totalgoal = str(row[0])
        return str(totalgoal)

    def totaldid(self):
        mydb = mysql.connector.connect(host="localhost", user="root", password='a1234567', database='flight_manager',
                                       auth_plugin='mysql_native_password')
        mycursor = mydb.cursor()
        query = """
                    select count(personal_num)
                    from flight_manager.staffing;
                        """
        mycursor.execute(query)
        results = mycursor.fetchall()
        mydb.commit()
        for row in results:
            totaldid = str(row[0])
        if totaldid == None:
            totaldid = '0'
        return str(totaldid)

    def deletegoals(self):
        mydb = mysql.connector.connect(host="localhost", user="root", password='a1234567', database='flight_manager',
                                       auth_plugin='mysql_native_password')
        mycursor = mydb.cursor()
        query = """
        delete from flight_manager.goals
        where status = 'azach' or status = 'miluim' ;

                                """
        mycursor.execute(query)
        mydb.commit()

    def deletejob(self, flight_date, flight_type):
        args = (flight_date, flight_type,)
        mydb = mysql.connector.connect(host="localhost", user="root", password='a1234567', database='flight_manager',
                                       auth_plugin='mysql_native_password')
        mycursor = mydb.cursor()
        query = """
                delete from flight_manager.shifts
                where flight_date = %s and flight_type = %s ;

                                        """
        mycursor.execute(query, args)
        mydb.commit()






        






