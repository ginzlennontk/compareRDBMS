import sqlite3
import csv
import time

class TestSqlite:
    def init(self):
        self.con = sqlite3.connect('test_sqlite.db')
        self.cur = self.con.cursor()   
        self.cur.execute("CREATE TABLE Subject(SubjectID VARCHAR(20) not null, \
                                               CourseTitle text, \
                                               Credit int not null, \
                                               SubjectGroup text, \
                                               PRIMARY KEY ( SubjectID ));")
        
        self.cur.execute("CREATE TABLE Student(StudentID VARCHAR(20) not null, \
                                               Fname text, \
                                               Lname text, \
                                               Faculty text, \
                                               Major text, \
                                               PRIMARY KEY ( StudentID ));")

        self.cur.execute("CREATE TABLE Registration( \
                                               StudentID VARCHAR(20) not null, \
                                               SubjectID VARCHAR(20) not null, \
                                               CourseTitle text, \
                                               Credit int not null, \
                                               Grade text not null, \
                       FOREIGN KEY (StudentID) references Student(StudentID), \
                       FOREIGN KEY (SubjectID) references Subject(SubjectID));")

    def import_csv(self):
        
        subject_file = csv.reader(open('subject.csv',encoding="utf8"),
                                  delimiter=',')
        for row in subject_file:
            self.cur.execute(   'insert into Subject \
                            (SubjectID, CourseTitle, Credit, SubjectGroup) \
                            values (?, ?, ?, ?)', row)

        student_file = csv.reader(open('student.csv', encoding="utf8"),
                                  delimiter=',')
        for row in student_file:
            self.cur.execute(   'insert into Student \
                            (StudentID, Fname, Lname, Faculty, Major) \
                            values (?, ?, ?, ?, ?)', row)
        
        regis_file = csv.reader(open('registration.csv', encoding="utf8"),
                                delimiter=',')
        for row in regis_file:
            self.cur.execute(   'insert into Registration \
                            (StudentID, SubjectID, CourseTitle, Credit, Grade) \
                            values (?, ?, ?, ?, ?)', row)
        
        self.con.commit()

    def query(self,command):
        self.cur.execute(str(command))
        self.cur.fetchall()


t = TestSqlite()
t.init()

start = time.time()
t.import_csv()
end = time.time()
import_time = end - start

start = time.time()
t.query("   SELECT StudentID, Fname, Lname FROM Student \
            WHERE Fname LIKE 'j%' OR Fname LIKE 'f%' OR Fname LIKE 'k%'")
end = time.time()
query1_time = end - start

start = time.time()
t.query("   SELECT StudentID FROM Registration \
            WHERE NOT Grade='A' AND CourseTitle='PROGRAMMING FUNDAMENTALS';")
end = time.time()
query2_time = end - start

start = time.time()
t.query("   SELECT subjectID, CourseTitle, COUNT(Grade) AS Number_of_A \
            FROM Registration \
            WHERE Grade = 'A' \
            GROUP BY subjectID \
            ORDER BY COUNT(Grade) DESC;")
end = time.time()
query3_time = end - start

print("Import Time : ", import_time, " Sec")
print("Query 1 Time : ", query1_time, " Sec")
print("Query 2 Time : ", query2_time, " Sec")
print("Query 3 Time : ", query3_time, " Sec")
