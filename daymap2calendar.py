from __future__ import print_function
import requests
import pandas as pd
from requests_ntlm import HttpNtlmAuth
import re
import math
import time
import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
import calendar

# parse timetable into list
def parseTimetable(timetable):
    timetable_data = pd.read_html(timetable)
    table = timetable_data[0]
    weekdays = list(table)
    for day in weekdays:
        index = weekdays.index(day)
        if index != 0:
            dayData = []
            lessonCounter = 1
            for lesson in table[day]:
                if lesson == lesson: # check if lesson is a free, or as Pandas says, NaN (not a number). if it is NaN, it will return false
                    # parse room, subject name and teacher from the lesson data
                    room = re.findall(r'[0-9][A-Z][A-Z][0-9][0-9]', str(lesson))[0]
                    name = re.findall(rf'^.+?(?={room})', str(lesson))[0]
                    teacher = re.findall(rf'(?<={room}).*', str(lesson))[0].strip()

                    # add data to list, which is appended to another list of subjects for that day
                    data = [lessonCounter, room, name, teacher]
                    dayData.append(data)

                lessonCounter = lessonCounter + 1
            # append data for the day to the complete week list
            sorted_data.append(dayData)
    print(sorted_data)
    return sorted_data

def googleAuth():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)

def findMonday(year):
    cal = calendar.Calendar(0)
    month = cal.monthdatescalendar(year, 1)
    lastweek = month[-1]
    monday = lastweek[0]
    return monday

def calculateSubjectTime(lesson, day):
    lessonLine = lesson[0]
    today = datetime.datetime.now()
    monday = findMonday(today.year)
    if lessonLine == 1: # HG Wednesday
        date = monday + datetime.timedelta(days=2)
        startTime = datetime.datetime.combine(date, datetime.time(9, 50))
        endTime = datetime.datetime.combine(date, datetime.time(10, 00))
        return [startTime.isoformat(), endTime.isoformat()]
    elif lessonLine == 3: # HG Monday & Friday
        if day == 0: # Monday
            date = monday
        elif day == 4: # Friday
            date = monday + datetime.timedelta(days=4)
            
        startTime = datetime.datetime.combine(date, datetime.time(8, 45))
        endTime = datetime.datetime.combine(date, datetime.time(8, 55))
        return [startTime.isoformat(), endTime.isoformat()]

    elif lessonLine == 4: # Lesson 1 (every day)
        if day == 0:
            date = monday
            startTime = datetime.datetime.combine(date, datetime.time(8, 55))
            endTime = datetime.datetime.combine(date, datetime.time(9, 50))
            return [startTime.isoformat(), endTime.isoformat()]
        elif day == 1: 
            date = monday + datetime.timedelta(days=day)
            startTime = datetime.datetime.combine(date, datetime.time(8, 45))
            endTime = datetime.datetime.combine(date, datetime.time(9, 50))
            return [startTime.isoformat(), endTime.isoformat()]
        elif day == 2:
            date = monday + datetime.timedelta(days=day)
            startTime = datetime.datetime.combine(date, datetime.time(10, 00)) 
            endTime = datetime.datetime.combine(date, datetime.time(11, 00))
            return [startTime.isoformat(), endTime.isoformat()]
        elif day == 3:
            date = monday + datetime.timedelta(days=day)
            startTime = datetime.datetime.combine(date, datetime.time(8, 45))
            endTime = datetime.datetime.combine(date, datetime.time(9, 50)) 
            return [startTime.isoformat(), endTime.isoformat()]
        elif day == 4:
            date = monday  + datetime.timedelta(days=day)
            startTime = datetime.datetime.combine(date, datetime.time(8, 55))
            endTime = datetime.datetime.combine(date, datetime.time(10, 15))
            return [startTime.isoformat(), endTime.isoformat()]
    elif lessonLine == 5: # Lesson 2 (Mon, Tue, Thurs)
        if day == 0:
            date = monday
            startTime = datetime.datetime.combine(date, datetime.time(9, 50))
            endTime = datetime.datetime.combine(date, datetime.time(10, 45))
            return [startTime.isoformat(), endTime.isoformat()]
        elif day == 1:
            date = monday + datetime.timedelta(days=day)
            startTime = datetime.datetime.combine(date, datetime.time(9, 50))
            endTime = datetime.datetime.combine(date, datetime.time(10, 50))
            return [startTime.isoformat(), endTime.isoformat()]
        elif day == 3:
            date = monday + datetime.timedelta(days=day)
            startTime = datetime.datetime.combine(date, datetime.time(9, 50))
            endTime = datetime.datetime.combine(date, datetime.time(10, 50))
            return [startTime.isoformat(), endTime.isoformat()]
    elif lessonLine == 7: # Lesson 2 (Wed, Fri)
        date = monday + datetime.timedelta(days=day)
        if day == 2:
            startTime = datetime.datetime.combine(date, datetime.time(11, 25))
            endTime = datetime.datetime.combine(date, datetime.time(12, 15))
            return [startTime.isoformat(), endTime.isoformat()]
        elif day == 4:
            startTime = datetime.datetime.combine(date, datetime.time(10, 40))
            endTime = datetime.datetime.combine(date, datetime.time(12, 00))
            return [startTime.isoformat(), endTime.isoformat()]
    elif lessonLine == 8: # Lesson 3 (every day)
        if day == 0: # Monday
            date = monday
            startTime = datetime.datetime.combine(date, datetime.time(11, 10))
            endTime = datetime.datetime.combine(date, datetime.time(12, 15))
            return [startTime.isoformat(), endTime.isoformat()]
        elif day == 1: # Tuesday
            date = monday + datetime.timedelta(days=day)
            startTime = datetime.datetime.combine(date, datetime.time(11, 15))
            endTime = datetime.datetime.combine(date, datetime.time(12, 5))
            return [startTime.isoformat(), endTime.isoformat()]
        elif day == 2: # Wednesday
            date = monday + datetime.timedelta(days=day)
            startTime = datetime.datetime.combine(date, datetime.time(11, 25)) 
            endTime = datetime.datetime.combine(date, datetime.time(12, 15))
            return [startTime.isoformat(), endTime.isoformat()]
        elif day == 3: # Thursday
            date = monday + datetime.timedelta(days=day)
            startTime = datetime.datetime.combine(date, datetime.time(11, 15))
            endTime = datetime.datetime.combine(date, datetime.time(12, 30))
            return [startTime.isoformat(), endTime.isoformat()]
        elif day == 4: # Friday
            date = monday  + datetime.timedelta(days=day)
            startTime = datetime.datetime.combine(date, datetime.time(10, 40))
            endTime = datetime.datetime.combine(date, datetime.time(12, 0))
            return [startTime.isoformat(), endTime.isoformat()]
    elif lessonLine == 9: # Lesson 4 (Mon, Tue, Thurs)
        if day == 0:
            date = monday
            startTime = datetime.datetime.combine(date, datetime.time(12, 15))
            endTime = datetime.datetime.combine(date, datetime.time(13, 20))
            return [startTime.isoformat(), endTime.isoformat()]
        elif day == 1:
            date = monday + datetime.timedelta(days=day)
            startTime = datetime.datetime.combine(date, datetime.time(12, 5))
            endTime = datetime.datetime.combine(date, datetime.time(13, 20))
            return [startTime.isoformat(), endTime.isoformat()]
        elif day == 3:
            date = monday + datetime.timedelta(days=day)
            startTime = datetime.datetime.combine(date, datetime.time(12, 30))
            endTime = datetime.datetime.combine(date, datetime.time(13, 20))
            return [startTime.isoformat(), endTime.isoformat()]
    elif lessonLine == 13 or lessonLine == 12: # Lesson 5 (Mon, Tue, Thurs) and Lesson 4 (Wed, Fri)
        if day == 0:
            date = monday
        else:
            date = monday + datetime.timedelta(days=day) 
        
        startTime = datetime.datetime.combine(date, datetime.time(14, 5))
        endTime = datetime.datetime.combine(date, datetime.time(15, 25))

        return [startTime.isoformat(), endTime.isoformat()]
    else: # 15, a.k.a Line 0. These aren't common, hence the else. also makes code simpler
        print("last")

def publishClassesToGoogle(service):
    print("Sending classes to Google Calendar. Please wait...")
    dayCount = 0
    for day in sorted_data:
        for newClass in day:
            newEvent = event
            newEvent["summary"] = newClass[2]
            newEvent["description"] = f"{newClass[3]} in {newClass[1]}"
            # calculate lesson time during the day
            times = calculateSubjectTime(newClass, dayCount)
            finalTimes = []
            for i in times:
                if time.localtime().tm_isdst == 0:
                    i += "+09:30"
                else:
                    i += "+10:30"
                finalTimes.append(i)

            newEvent["start"]["dateTime"] = finalTimes[0]
            newEvent["start"]["timeZone"] = "Australia/Adelaide"
            newEvent["end"]["dateTime"] = finalTimes[1]
            newEvent["end"]["timeZone"] = "Australia/Adelaide"
            newEvent["recurrence"] = ['RRULE:FREQ=WEEKLY;COUNT=40']
            print(newEvent)

        dayCount = dayCount + 1


validLines = [1,3,4,5,7,8,9,12,13,15] # only these rows in daymap's timetable contain lessons
sorted_data = []

# google api scope. r/w access to events is all thats needed
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

# google event JSON template
event = {
  'summary': '',
  'location': '',
  'description': '',
  'start': {
    'dateTime': '',
    'timeZone': '',
  },
  'end': {
    'dateTime': '2015-05-28T17:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'recurrence': [
    'RRULE:FREQ=DAILY;COUNT=2'
  ],
  'attendees': [
    {'email': 'lpage@example.com'},
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}

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
    print("Welcome, you are logged in. Locating and parsing classes...")
    parsedTimetable = parseTimetable(timetable.text)
    print("Classes found. Logging in to Google...")
    googleService = googleAuth()
    print("Logged in. Uploading classes to Google Calendar...")
    publishClassesToGoogle(googleService)
    print("Classes uploaded. Thank you for using Daymap2Calendar!")

else:
    print(f"Login failed, try again later. Quitting... (error code: {timetable.status_code} {assessment.status_code})")
    time.sleep(2)