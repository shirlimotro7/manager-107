

import mysql.connector
from django.contrib.auth.models import User
from datetime import datetime
from mysite.shift import Shift
from mysite.air_crew import AirCrew
from mysite.contact import Contact


mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319", password = 'c786913f', database = 'heroku_947e29c06a5b4a3')
from mysite.shift import Shift
class ShiftManager():
    def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.personal_num = ""



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
        mycursor.close()
        name = []
        for row in results:
            first_name = row[0]
            last_name = row[1]
            name.append(first_name.capitalize())
            name.append(last_name.capitalize())
        return name[0] +' '+ name[1]

    def insertshift(self, date, type, notes):
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

        val = (date, type, notes,)
        mycursor = mydb.cursor()
        query = """ insert into shifts(flight_date,flight_type, notes)
                            VALUES(%s,%s,%s)"""
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()

    def insertgoals(self, azach_num, miluim_num):
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

        val1 = (azach_num,)
        val2 =  (miluim_num,)
        mycursor = mydb.cursor()
        query = """ insert into goals(status, goal)
                    VALUES('azach',%s );
                    
                """
        mycursor.execute(query, val1)
        mydb.commit()
        query2 = """
                    insert into goals(status, goal)
                    VALUES('miluim', %s )
                """
        mycursor.execute(query2, val2)
        mydb.commit()
        mycursor.close()

    def getletters(self):
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

        mycursor = mydb.cursor()
        query = """
                    select * from contact
               """
        mycursor.execute(query)
        results = mycursor.fetchall()
        mydb.commit()
        mycursor.close()
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
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

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

            
                """
        mycursor.execute(query)
        results = mycursor.fetchall()
        mydb.commit()
        mycursor.close()
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
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

        mycursor = mydb.cursor()
        query = """
            select air_crew.personal_number, auth_user.first_name, auth_user.last_name, 
            air_crew.goal, count(staffing.personal_num) As achieved
            from auth_user  join air_crew
            on auth_user.username = air_crew.personal_number
            left join staffing
            on air_crew.personal_number = staffing.personal_num
            group by air_crew.personal_number;
            
            """
        mycursor.execute(query)
        results = mycursor.fetchall()
        mydb.commit()
        mycursor.close()
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
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

        mycursor = mydb.cursor()
        query = """
            select count(personal_number) As num_of_people
            from air_crew
                """
        mycursor.execute(query)
        results = mycursor.fetchall()
        mydb.commit()
        mycursor.close()
        for row in results:
            num_of_crew = str(row[0])
        return num_of_crew

    def totalgoal(self):
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

        mycursor = mydb.cursor()
        query = """
                    select sum(goal) 
                    from air_crew
                        """
        mycursor.execute(query)
        results = mycursor.fetchall()
        mydb.commit()
        for row in results:
            totalgoal = str(row[0])
        return str(totalgoal)

    def totaldid(self):
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

        mycursor = mydb.cursor()
        query = """
                    select count(personal_num)
                    from staffing;
                        """
        mycursor.execute(query)
        results = mycursor.fetchall()
        mydb.commit()
        mycursor.close()
        for row in results:
            totaldid = str(row[0])
        if totaldid == None:
            totaldid = '0'
        return str(totaldid)

    def deletegoals(self):
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

        mycursor = mydb.cursor()
        query = """
        delete from goals
        where status = 'azach' or status = 'miluim' ;

                                """
        mycursor.execute(query)
        mydb.commit()
        mycursor.close()

    def deletejob(self, flight_date, flight_type):
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

        args = (flight_date, flight_type,)
        mycursor = mydb.cursor()
        query = """
                delete from shifts
                where flight_date = %s and flight_type = %s ;

                                        """
        mycursor.execute(query, args)
        mydb.commit()
        mycursor.close()

    def deletestaffing(self, flight_date, flight_type, personal_num):
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

        args = (flight_date, flight_type, personal_num,)
        mycursor = mydb.cursor()
        query = """
                delete from staffing
                where flight_date = %s and flight_type = %s and personal_num = %s 

                                        """
        mycursor.execute(query, args)
        mydb.commit()
        mycursor.close()
        mydb.close()


    def insert_auth(self, personal_num):
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

        val = (personal_num,)
        mycursor = mydb.cursor()
        query = """ insert into auth_air_crew(personal_num)
                            VALUES(%s)"""
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()

    def show_auth(self):
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')
        mycursor = mydb.cursor()
        query = """
            select auth_air_crew.personal_num
            from auth_air_crew 
            """
        mycursor.execute(query)
        results = mycursor.fetchall()
        mydb.commit()
        mycursor.close()
        personal_numbers = []
        for row in results:
            personal_num = str(row[0])
            personal_numbers.append(personal_num)
        return personal_numbers

    def delete_auth(self, personal_num):
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

        val = (personal_num,)
        mycursor = mydb.cursor()
        query = """
                delete from auth_air_crew
                where personal_num = %s ;

                                        """
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()

    def myweek(self):
        today = datetime.today().strftime('%Y-%m-%d')
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

        mycursor = mydb.cursor()
        query = """SELECT *
    FROM   shifts left join staffing 
    on staffing.flight_date = shifts.flight_date
    and staffing.flight_type = shifts.flight_type
    WHERE  YEARWEEK(shifts.flight_date) =   YEARWEEK(curdate());
                                 """
        mycursor.execute(query, )
        results = mycursor.fetchall()
        mydb.commit()
        mycursor.close()
        shifts = []
        for row in results:
            shift = Shift()
            shift.flight_date = str(row[0])
            shift.flight_type = str(row[1]).capitalize()
            shift.notes = str(row[2]).capitalize()
            if shift.flight_date < today:
                shift.status = 'Done'
            else:
                shift.status = "Not Done"
            shifts.append(shift)
        return shifts






        






