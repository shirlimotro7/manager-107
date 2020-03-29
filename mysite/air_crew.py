
import mysql.connector
from django.contrib.auth.models import User
from datetime import datetime
from mysite.shift import Shift

from mysite.shift import Shift
mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319", password = 'c786913f', database = 'heroku_947e29c06a5b4a3',auth_plugin='mysql_native_password')

class AirCrew():
    def __init__(self):
        self.personal_num = ""
        self.name = ""
        self.category = ""
        self.movil = ""
        self.goal = ""
        self.achieved = ""
        self.notes = ""
        self.status = ""


    def InsertToDb(self):
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

        air_crew = AirCrew
        if self.status == 'Azach':
            self.goal = air_crew.findgoalazach(self)
        elif self.status == 'Miluim':
            self.goal = air_crew.findgoalazach(self)
        val = (self.personal_num, self.movil, self.category, self.goal)
        mycursor = mydb.cursor()
        query = """ insert into air_crew(personal_number, leader, crew_role, goal)
                    VALUES(%s,%s,%s,%s)"""
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()


    def getall(self):
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

        mycursor = mydb.cursor()
        query = """select * from air_crew"""
        mycursor.execute(query)
        results = mycursor.fetchall()
        mydb.commit()
        mycursor.close()
        rows = []
        for row in results:
            person = AirCrew()
            person.personal_num = row[2]
            person.category = row[3]
            person.movil = row[4]
            rows.append(person)
        return rows

    def findgoalazach(self):
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

        mycursor = mydb.cursor()
        query = """
        SELECT goal
        FROM goals
        where status = 'azach'
            """
        mycursor.execute(query)
        results = mycursor.fetchall()
        mydb.commit()
        mycursor.close()
        goal1 = []
        for row in results:
            goal = str(row[0])
            goal1.append(goal)
        return str(goal1[0])

    def findgoalmiluim(self):
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

        mycursor = mydb.cursor()
        query = """
        SELECT goal
        FROM goals
        where status = 'miluim'
            """
        mycursor.execute(query)
        results = mycursor.fetchall()
        mydb.commit()
        mycursor.close()
        goal1 = []
        for row in results:
            goal = str(row[0])
            goal1.append(goal)
        return str(goal1[0])


    def ShowMyShifts(self, username):
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

        username = (username,)
        mycursor = mydb.cursor()
        query = """
         SELECT staffing.flight_date, staffing.flight_type, staffing.leader , shifts.notes
        FROM staffing join shifts 
        where staffing.flight_type = shifts.flight_type
        and staffing.flight_date = shifts.flight_date
        and personal_num= %s

        """
        mycursor.execute(query, username)
        results = mycursor.fetchall()
        mydb.commit()
        my_shifts = []
        for row in results:
            shift = Shift()
            shift.flight_date = str(row[0])
            shift.flight_type = str(row[1])
            shift.leader = str(row[2])
            shift.notes =  str(row[3])
            my_shifts.append(shift)
        return my_shifts

    def ShowFutureShifts(self, username):
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

        username = (username,)
        mycursor = mydb.cursor()
        query = """
         SELECT staffing.flight_date, staffing.flight_type, staffing.leader , shifts.notes
        FROM staffing join shifts 
        where staffing.flight_type = shifts.flight_type
        and staffing.flight_date = shifts.flight_date
        and personal_num= %s
        and staffing.flight_date > curdate();

        """
        mycursor.execute(query, username)
        results = mycursor.fetchall()
        mydb.commit()
        mycursor.close()
        future_shifts = []
        for row in results:
            shift = Shift()
            shift.flight_date = str(row[0])
            shift.flight_type = str(row[1])
            shift.leader = str(row[2])
            shift.notes =  str(row[3])
            future_shifts.append(shift)
        return future_shifts

    def getname(self, username):
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')
        mycursor = mydb.cursor()
        query = """
                 SELECT first_name, last_name FROM auth_user WHERE username= %s 
                """
        mycursor.execute(query, username)
        results = mycursor.fetchall()
        mydb.commit()
        name = []
        mycursor.close()
        for row in results:
            first_name = row[0]
            last_name = row[1]
            name.append(first_name.capitalize())
            name.append(last_name.capitalize())
        return name[0] +' '+ name[1]

    def CheckLeader(self, username):
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3',
                                       auth_plugin='mysql_native_password')
        username = (username,)
        mycursor = mydb.cursor()
        query = """
                         SELECT air_crew.leader FROM air_crew WHERE personal_number = %s 
                         and leader = '1'
                        """
        mycursor.execute(query, username)
        results = mycursor.fetchall()
        mydb.commit()
        mycursor.close()
        role = []
        for row in results:
            i = row[0]
            role.append(i)
        if len(role) > 0:
            return True
        else:
            return False


    def CheckPilot(self, username):
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

        username = (username,)
        mycursor = mydb.cursor()
        query = """
                         SELECT air_crew.crew_role FROM air_crew WHERE personal_number= %s
                         and crew_role = 'pilot' 
                        """
        mycursor.execute(query, username)
        results = mycursor.fetchall()
        mydb.commit()
        mycursor.close()
        role = []
        for row in results:
            row = row[0]
            role.append(row)
        if len(role) > 0:
            return True
        else:
            return False



    def ShowAvailableShiftsLeaders(self, status):
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

        arg = (status,)
        mycursor = mydb.cursor()
        query = """
       SELECT shifts.flight_date,  shifts.flight_type,  type_of_shift.crew_role,  type_of_shift.leader
        from shifts join type_of_shift
        on shifts.flight_type = type_of_shift.flight_type 
        left join staffing
        on shifts.flight_date = staffing.flight_date
        and type_of_shift.flight_type = staffing.flight_type
        and (type_of_shift.crew_role = staffing.crew_role
        or type_of_shift.crew_role = 'all')
        and type_of_shift.leader = staffing.leader
        where personal_num is NULL
        and (type_of_shift.crew_role = %s or type_of_shift.crew_role = 'all')
        and shifts.flight_date > CURDATE()
      

        """
        mycursor.execute(query, arg)
        results = mycursor.fetchall()
        mydb.commit()
        mycursor.close()
        available_shifts = []
        for row in results:
            shift = Shift()
            shift.flight_date = str(row[0])
            shift.flight_type = str(row[1])
            shift.crew_role = str(row[2])
            shift.leader = str(row[3])
            available_shifts.append(shift)
        return available_shifts


    def ShowAvailableShifts(self, status):
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

        arg = (status,)
        mycursor = mydb.cursor()
        query = """
        SELECT shifts.flight_date,  shifts.flight_type,  type_of_shift.crew_role,  type_of_shift.leader
        from shifts join type_of_shift
        on shifts.flight_type = type_of_shift.flight_type 
        left join staffing
        on shifts.flight_date = staffing.flight_date
        and type_of_shift.flight_type = staffing.flight_type
        and (type_of_shift.crew_role = staffing.crew_role
        or type_of_shift.crew_role = 'all')
        and type_of_shift.leader = staffing.leader
        where personal_num is NULL
        and (type_of_shift.crew_role = %s or type_of_shift.crew_role = 'all')
        and (type_of_shift.leader ='0' or type_of_shift.leader = '3')
        and shifts.flight_date > CURDATE()
        
        """
        mycursor.execute(query, arg)
        results = mycursor.fetchall()
        mydb.commit()
        mycursor.close()
        available_shifts1 = []
        for row in results:
            shift = Shift()
            shift.flight_date = str(row[0])
            shift.flight_type = str(row[1])
            shift.crew_role = str(row[2])
            shift.leader = str(row[3])
            available_shifts1.append(shift)
        return available_shifts1

    def howmanydid(self, username):
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

        mycursor = mydb.cursor()
        query = """select count(personal_num) from staffing where personal_num = %s
         """
        args = (username,)
        mycursor.execute(query,args)
        results = mycursor.fetchall()
        mydb.commit()
        mycursor.close()
        rows = []
        for row in results:
            number = row[0]
            rows.append(number)
        return rows


    def howmanytot(self, username):
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

        mycursor = mydb.cursor()
        query = """select count(personal_num) from staffing where personal_num = %s
         """
        mycursor.execute(query,username)
        results = mycursor.fetchall()
        mydb.commit()
        mycursor.close()
        rows = []
        for row in results:
            number = row[0]
            rows.append(number)
        return rows

    def is_auth(self, username):
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3',
                                       auth_plugin='mysql_native_password')
        username = (username,)
        mycursor = mydb.cursor()
        query = """
                         SELECT auth_air_crew.personal_num 
                         FROM auth_air_crew WHERE personal_num = %s       
                        """
        mycursor.execute(query, username)
        results = mycursor.fetchall()
        mydb.commit()
        mycursor.close()
        role = []
        for row in results:
            i = row[0]
            role.append(i)
        if len(role) > 0:
            return True
        else:
            return False













