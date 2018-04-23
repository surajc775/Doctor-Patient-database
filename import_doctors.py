import sys
import csv
from bs4 import BeautifulSoup
import pymysql.cursors
import json

xml_file = ''
csv_file = ''
json_file = ''



if __name__=="__main__":
    
    for filename in sys.argv:
        if ".xml" in filename:
            xml_file = filename
        elif ".csv" in filename:
            csv_file = filename
        elif ".json" in filename:
            json_file = filename

    #print(xml_file)

    infile = open(xml_file, 'r')
    contents = infile.read()
    #print(contents)
    soup = BeautifulSoup(contents, 'xml')
    #print(soup)
    firstNames = soup.find_all('firstName')
    lastNames = soup.find_all('lastName')
    specialties = soup.find_all('specialty')

    #print(firstNames)
    #print(specialties)

    doctorInfo = []
    doctorIds = []

    for num in range(len(firstNames)):
        doc = [firstNames[num].get_text(), lastNames[num].get_text(), specialties[num].get_text()]
        doctorInfo.append(doc)

    #print(doctorInfo)



    connection = pymysql.connect(host='localhost', user='root', password='', db='doctors', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    print("connection made")

    try:
        with connection.cursor() as cursor:
        # truncate all tables, to clear the data
            sql = "delete from visit"
            cursor.execute(sql)
            sql = "delete from patient"
            cursor.execute(sql)
            sql = "delete from doctor"
            cursor.execute(sql)

            connection.commit()

        with connection.cursor() as cursor:
           # Create a new record
            sql = "INSERT INTO doctor (first_name, last_name, specialty) VALUES (%s, %s, %s)"
            

            for counter, person in enumerate(doctorInfo,1 ):
                doctorIds.append([counter, person[0]])
                cursor.execute(sql, (person[0], person[1], person[2]))
                #connection.commit()

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

        with open(csv_file, 'r') as toon:
            csvin = csv.reader(toon)
            patients = [line for line in csvin]

        patientFirstLast = [patient[0].split(' ') for patient in patients[1:]]
        patientProvider = [patient[1].split(' ') for patient in patients[1:]]
        zipped = zip(patientFirstLast, patientProvider)
        finalPatients = list(zipped)
        patientReader = []
        print(finalPatients)

        with connection.cursor() as cursor:
        # Read a single record
            sql = "SELECT doctor_id, first_name FROM doctor"
            #cursor.execute(sql, ('webmaster@python.org')) example txt
            
            
            cursor.execute(sql)
            
            for row in cursor:
                print(row)
                for n in finalPatients:
                    print(n[1][0])
                    if(row['first_name'] == n[1][0]):
                        n[0].append(row['doctor_id'])
                        patientReader.append(n[0])
            
            sql = "INSERT INTO patient (first_name, last_name, doctor_id) VALUES (%s, %s, %s)"
            #cursor.execute(sql, (10, "suraj", 'chatarathi'))
            connection.commit()
            print(patientReader)
            for counter, person in enumerate(patientReader, 1):
                cursor.execute(sql, (person[0], person[1], person[2]))
            connection.commit()

        file = json.load(open(json_file))

        with connection.cursor() as cursor:
            sql = "SELECT doctor_id, first_name FROM doctor"

            visits = []
            for person in file.keys():
                for date in file[person].keys():
                    a,b = person.split()
                    c,d = file[person][date].split()
                    alist = []
                    alist.append(a)
                    alist.append(b)
                    alist.append(date)
                    alist.append(c)
                    alist.append(d)
                    visits.append(alist)

            finalVisits = []
            cursor.execute(sql)
            for row in cursor:
                for n in visits:
                    if(n[3] == row['first_name']):
                        n.append(row['doctor_id'])
                        finalVisits.append(n)

            sql = "SELECT patient_id, first_name FROM patient"

            exeVisits = []
            cursor.execute(sql)
            for row in cursor:
                for n in finalVisits:
                    if(n[0] == row['first_name']):
                        n.append(row['patient_id'])
                        exeVisits.append(n)

            sql = "INSERT INTO visit (doctor_id, patient_id, visit_date) VALUES (%s, %s, %s)"
            for visit in exeVisits:
                cursor.execute(sql, (visit[5], visit[6], visit[2]))
                
            print(exeVisits)
            connection.commit()
    finally:
        connection.close()
    


