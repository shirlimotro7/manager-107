from datetime import datetime
import mysql.connector



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

    def getname(self, username):
        try:
            username = (username,)
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
                first_name = row[0].capitalize()
                last_name = row[1].capitalize()
                name.append(first_name)
                name.append(last_name)
            return name[0] + ' ' + name[1]
        except:
            return "NoName"



    def ShowAllShifts(self):
        today = datetime.today().strftime('%Y-%m-%d')
        mydb = mysql.connector.connect(host="localhost", user="root", password='a1234567', database='flight_manager',
                                       auth_plugin='mysql_native_password')
        mycursor = mydb.cursor()
        query = """select flight_date, shifts.flight_type, crew_role, leader
            from flight_manager.shifts  inner join flight_manager.type_of_shift 
            where flight_manager.shifts.flight_type = flight_manager.type_of_shift.flight_type
            and flight_manager.shifts.flight_date > %s """
        mycursor.execute(query, (today,))
        results = mycursor.fetchall()
        mydb.commit()
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
            shifts.append(shift)
        return shifts

    def ShowAllStaffing(self):
        mydb = mysql.connector.connect(host="localhost", user="root", password='a1234567', database='flight_manager',
                                       auth_plugin='mysql_native_password')
        mycursor = mydb.cursor()
        query = """select  *
               from flight_manager.staffing  """
        mycursor.execute(query)
        results = mycursor.fetchall()
        mydb.commit()
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
        val = (flight_date, flight_type, personal_num, crew_role, leader,)
        mydb = mysql.connector.connect(host="localhost", user="root", password='a1234567', database='flight_manager',
                                       auth_plugin='mysql_native_password')
        mycursor = mydb.cursor()
        query = """ insert into flight_manager.staffing(flight_date, flight_type, personal_num, crew_role, leader)
                            VALUES(%s,%s,%s,%s,%s)"""
        mycursor.execute(query, val)
        mydb.commit()

    def showalljobs(self):
        mydb = mysql.connector.connect(host="localhost", user="root", password='a1234567', database='flight_manager',
                                       auth_plugin='mysql_native_password')
        mycursor = mydb.cursor()
        query = """select  *
                       from flight_manager.shifts  """
        mycursor.execute(query)
        results = mycursor.fetchall()
        mydb.commit()
        shifts = []
        for row in results:
            shift = Shift()
            shift.flight_date = str(row[0])
            shift.flight_type = str(row[1]).capitalize()
            shift.notes = str(row[2]).capitalize()
            shifts.append(shift)
        return shifts









