import sqlite3
import random
import os
import string
import sys

def generate_word(length):
    VOWELS = "aeiou"
    CONSONANTS = "".join(set(string.ascii_lowercase) - set(VOWELS))
    word = ""
    for i in range(length):
        if i % 2 == 0:
            word += random.choice(CONSONANTS)
        else:
            word += random.choice(VOWELS)
    return word

grade = ["A","B+","B","C+","C","D+","D"]
con = sqlite3.connect('test.db')
i = 200000
for j in range(i):
    student_id = str(j+1).zfill(12)
    name = generate_word(6)
    surname = generate_word(6)
    con.execute("INSERT INTO Student (StudentID,Fname,Lname,Faculty,Major) \
      VALUES ('"+student_id+"', '"+name+"', '"+surname+"', 'วิศวกรรมศาสตร์', 'วิศวกรรมคอมพิวเตอร์')")

    cursor = con.execute("SELECT SubjectID, CourseTitle, Credit,SubjectGroup from Subject")
    for row in cursor:
        con.execute("INSERT INTO Registration (StudentID,SubjectID, CourseTitle, Credit,Grade) \
      VALUES ('"+student_id+"', '"+row[0]+"','"+row[1]+"', "+str(row[2])+", '"+grade[random.randint(0,len(grade)-1)]+"')")

con.commit()
