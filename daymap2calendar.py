import requests
import pandas as pd
from requests_ntlm import HttpNtlmAuth
from bs4 import BeautifulSoup
import re
import math
import time

# parse timetable into list
def parseTimetable(timetable):
    timetable_data = pd.read_html(timetable)
    table = timetable_data[0]
    weekdays = list(table)
    for day in weekdays:
        index = weekdays.index(day)
        if index != 0:
            dayData = []
            count = 0
            for lesson in table[day]:
                if lesson == lesson: # check if lesson is a free, or as Pandas says, NaN (not a number). if it is NaN, it will return false
                    # parse room, subject name and teacher from the lesson data
                    room = re.findall(r'[0-9][A-Z][A-Z][0-9][0-9]', str(lesson))[0]
                    name = re.findall(rf'^.+?(?={room})', str(lesson))[0]
                    teacher = re.findall(rf'(?<={room}).*', str(lesson))[0].strip()

                    # add data to list, which is appended to another list of subjects for that day
                    data = [room, name, teacher]
                    dayData.append(data)

                    count = count + 1
            # append data for the day to the complete week list
            sorted_data.append(dayData)
    return sorted_data

def googleAuth():
    print("google auth")

validLines = [1,3,4,5,7,8,9,12,13,15] # only these rows in daymap's timetable contain lessons
sorted_data =[]

#username and password
username = input(r"Enter Daymap username (e.g. domain\firstname.lastname): ")
print(rf'{username}')
password = input("Enter Daymap password: ")

print("Logging in. Please wait...")

session = requests.Session()
session.auth = HttpNtlmAuth(rf'{username}',rf'{password}')
timetable = session.get('http://daymap.gihs.sa.edu.au/timetable/timetable.aspx')
assessment = session.get("http://daymap.gihs.sa.edu.au/student/assessmentsummary.aspx")

if timetable.status_code == 200 and assessment.status_code == 200:
    print("status 200 OK, proceeding to parse ASPX...")
    parsedTimetable = parseTimetable(timetable.text))

else:
    print(f"Login failed, try again later. Quitting... (error code: {timetable.status_code} {assessment.status_code})")
    time.sleep(2)