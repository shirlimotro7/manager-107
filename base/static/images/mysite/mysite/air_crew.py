
import mysql.connector
from django.contrib.auth.models import User
from datetime import datetime
from mysite.shift import Shift

mydb = mysql.connector.connect(host="localhost", user="root", password = 'a1234567', database = 'flight_manager',auth_plugin='mysql_native_password')
from mysite.shift import Shift

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
        air_crew = AirCrew
        if self.status == 'Azach':
            self.goal = air_crew.findgoalazach(self)
        elif self.status == 'Miluim':
            self.goal = air_crew.findgoalazach(self)
        val = (self.personal_num, self.movil, self.category, self.goal)
        mydb = mysql.connector.connect(host="localhost", user="root", password='a1234567', database='flight_manager',
                                       auth_plugin='mysql_native_password')
        mycursor = mydb.cursor()
        query = """ insert into air_crew(personal_number, leader, crew_role, goal)
                    VALUES(%s,%s,%s,%s)"""
        mycursor.execute(query, val)
        mydb.commit()


    def getall(self):
        mydb = mysql.connector.connect(host="localhost", user="root", password='a1234567', database='flight_manager',
                                       auth_plugin='mysql_native_password')
        mycursor = mydb.cursor()
        query = """select * from flight_manager.air_crew"""
        mycursor.execute(query)
        results = mycursor.fetchall()
        mydb.commit()
        rows = []
        for row in results:
            person = AirCrew()
            person.personal_num = row[2]
            person.category = row[3]
            person.movil = row[4]
            rows.append(person)
        return rows

    def findgoalazach(self):
        mydb = mysql.connector.connect(host="localhost", user="root", password='a1234567', database='flight_manager',
                                       auth_plugin='mysql_native_password')
        mycursor = mydb.cursor()
        query = """
        SELECT goal
        FROM flight_manager.goals
        where status = 'azach'
            """
        mycursor.execute(query)
        results = mycursor.fetchall()
        mydb.commit()
        goal1 = []
        for row in results:
            goal = str(row[0])
            goal1.append(goal)
        return str(goal1[0])

    def findgoalmiluim(self):

        mydb = mysql.connector.connect(host="localhost", user="root", password='a1234567', database='flight_manager',
                                       auth_plugin='mysql_native_password')
        mycursor = mydb.cursor()
        query = """
        SELECT goal
        FROM flight_manager.goals
        where status = 'miluim'
            """
        mycursor.execute(query)
        results = mycursor.fetchall()
        mydb.commit()
        goal1 = []
        for row in results:
            goal = str(row[0])
            goal1.append(goal)
        return str(goal1[0])



        
        
        
        
        
        
    def ShowMyShifts(self, username):
        username = (username,)
        mydb = mysql.connector.connect(host="localhost", user="root", password='a1234567', database='flight_manager',
                                       auth_plugin='mysql_native_password')
        mycursor = mydb.cursor()
        query = """
         SELECT flight_manager.staffing.flight_date, flight_manager.staffing.flight_type, flight_manager.staffing.leader , shifts.notes
        FROM flight_manager.staffing join flight_manager.shifts 
        where flight_manager.staffing.flight_type = flight_manager.shifts.flight_type
        and flight_manager.staffing.flight_date = flight_manager.shifts.flight_date
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
        username = (username,)
        mydb = mysql.connector.connect(host="localhost", user="root", password='a1234567', database='flight_manager',
                                       auth_plugin='mysql_native_password')
        mycursor = mydb.cursor()
        query = """
         SELECT flight_manager.staffing.flight_date, flight_manager.staffing.flight_type, flight_manager.staffing.leader , shifts.notes
        FROM flight_manager.staffing join flight_manager.shifts 
        where flight_manager.staffing.flight_type = flight_manager.shifts.flight_type
        and flight_manager.staffing.flight_date = flight_manager.shifts.flight_date
        and personal_num= %s
        and flight_manager.staffing.flight_date > curdate();

        """
        mycursor.execute(query, username)
        results = mycursor.fetchall()
        mydb.commit()
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

    def CheckLeader(self, username):
        username = (username,)
        mydb = mysql.connector.connect(host="localhost", user="root", password='a1234567', database='flight_manager',
                                       auth_plugin='mysql_native_password')
        mycursor = mydb.cursor()
        query = """
                         SELECT flight_manager.air_crew.leader FROM flight_manager.air_crew WHERE personal_number = %s 
                         and leader = '1'
                        """
        mycursor.execute(query, username)
        results = mycursor.fetchall()
        mydb.commit()
        role = []
        for row in results:
            i = row[0]
            role.append(i)
        if len(role) > 0:
            return True
        else:
            return False


    def CheckPilot(self, username):
        username = (username,)
        mydb = mysql.connector.connect(host="localhost", user="root", password='a1234567', database='flight_manager',
                                       auth_plugin='mysql_native_password')
        mycursor = mydb.cursor()
        query = """
                         SELECT flight_manager.air_crew.crew_role FROM flight_manager.air_crew WHERE personal_number= %s
                         and crew_role = 'pilot' 
                        """
        mycursor.execute(query, username)
        results = mycursor.fetchall()
        mydb.commit()
        role = []
        for row in results:
            row = row[0]
            role.append(row)
        if len(role) > 0:
            return True
        else:
            return False



    def ShowAvailableShiftsLeaders(self, status):
        arg = (status,)
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
        and (type_of_shift.crew_role = %s or type_of_shift.crew_role = 'all')
        and flight_manager.shifts.flight_date > CURDATE()
      

        """
        mycursor.execute(query, arg)
        results = mycursor.fetchall()
        mydb.commit()
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
        arg = (status,)
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
        and (type_of_shift.crew_role = %s or type_of_shift.crew_role = 'all')
        and (type_of_shift.leader ='0' or type_of_shift.leader = '3')
        and flight_manager.shifts.flight_date > CURDATE()
        
        """
        mycursor.execute(query, arg)
        results = mycursor.fetchall()
        mydb.commit()
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
        mydb = mysql.connector.connect(host="localhost", user="root", password='a1234567', database='flight_manager',
                                       auth_plugin='mysql_native_password')
        mycursor = mydb.cursor()
        query = """select count(personal_num) from flight_manager.staffing where personal_num = %s
         """
        args = (username,)
        mycursor.execute(query,args)
        results = mycursor.fetchall()
        mydb.commit()
        rows = []
        for row in results:
            number = row[0]
            rows.append(number)
        return rows


    def howmanytot(self, username):
        mydb = mysql.connector.connect(host="localhost", user="root", password='a1234567', database='flight_manager',
                                       auth_plugin='mysql_native_password')
        mycursor = mydb.cursor()
        query = """select count(personal_num) from flight_manager.staffing where personal_num = %s
         """
        mycursor.execute(query,username)
        results = mycursor.fetchall()
        mydb.commit()
        rows = []
        for row in results:
            number = row[0]
            rows.append(number)
        return rows












