from datetime import datetime
import mysql.connector

mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319", password = 'c786913f', database = 'heroku_947e29c06a5b4a3',auth_plugin='mysql_native_password')


class Shift():
    def __init__(self):
        self.flight_date = ""
        self.flight_type = ""
        self.crew_role = ""
        self.leader = ""
        self.personal_num = ""
        self.aircrew_name = ""
        self.number = ""
        self.notes = ""
        self.status = ""

    def getname(self, username):
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')
        try:
            username = (username,)
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
                first_name = row[0].capitalize()
                last_name = row[1].capitalize()
                name.append(first_name)
                name.append(last_name)
            return name[0] + ' ' + name[1]
        except:
            return "NoName"


    def ShowAllShifts(self):
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

        today = datetime.today().strftime('%Y-%m-%d')
        mycursor = mydb.cursor()
        query = """select flight_date, shifts.flight_type, crew_role, leader
            from shifts  inner join type_of_shift 
            where shifts.flight_type = type_of_shift.flight_type
             """
        mycursor.execute(query,)
        results = mycursor.fetchall()
        mydb.commit()
        mycursor.close()
        shifts = []
        for row in results:
            shift = Shift()
            shift.flight_date = str(row[0])
            shift.flight_type = str(row[1])
            shift.crew_role = str(row[2]).capitalize()
            if str(row[3]) == '0':
                shift.leader = str('Number 2')
            elif str(row[3]) == '1':
                 shift.leader = str('Must Be Movil')
            elif str(row[3]) == '3':
                shift.leader = str('ALL')
            else:
                shift.leader = str(row[3])
            if shift.flight_date < today:
                shift.status = 'Done'
            else :
                shift.status = "Not Done"
            shifts.append(shift)
        return shifts

    def ShowAllStaffing(self):
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

        mycursor = mydb.cursor()
        query = """select  *
               from staffing  """
        mycursor.execute(query)
        results = mycursor.fetchall()
        mydb.commit()
        mycursor.close()
        shifts = []
        for row in results:
            shift = Shift()
            shift.flight_date = str(row[0])
            shift.flight_type = str(row[1]).capitalize()
            shift.personal_num = str(row[2])
            shift.aircrew_name = shift.getname(str(shift.personal_num))
            shift.crew_role = str(row[3])
            if str(row[4]) =='1':
                shift.leader = 'Must Be Movil'
            elif str(row[4]) == '0':
                shift.leader = 'Number 2'
            else :
                shift.leader = 'All'
            shifts.append(shift)
        return shifts

    def InsertToStaffing(self, flight_date, flight_type, personal_num, crew_role, leader):
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

        val = (flight_date, flight_type, personal_num, crew_role, leader,)
        mycursor = mydb.cursor()
        query = """ insert into staffing(flight_date, flight_type, personal_num, crew_role, leader)
                            VALUES(%s,%s,%s,%s,%s)"""
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()

    def showalljobs(self):
        today = datetime.today().strftime('%Y-%m-%d')
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

        mycursor = mydb.cursor()
        query = """select  *
                       from shifts
                         """
        mycursor.execute(query,)
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

    def showalljobstype(self):
        today = datetime.today().strftime('%Y-%m-%d')
        mydb = mysql.connector.connect(host="us-cdbr-iron-east-01.cleardb.net", user="bc066a0258e319",
                                       password='c786913f', database='heroku_947e29c06a5b4a3')

        mycursor = mydb.cursor()
        query = """select  *
                       from shifts
                       order by flight_type
                         """
        mycursor.execute(query,)
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









