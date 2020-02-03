from __future__ import print_function
import requests
import pandas as pd
from requests_ntlm import HttpNtlmAuth
from bs4 import BeautifulSoup
import re
import math
import time
import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

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

def publishClassesToGoogle(service):
    print("Sending classes to Google Calendar. Please wait...")


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
    print("status 200 OK, proceeding to parse ASPX...")
    parsedTimetable = parseTimetable(timetable.text)
    googleService = googleAuth()
    publishClassesToGoogle(googleService)

else:
    print(f"Login failed, try again later. Quitting... (error code: {timetable.status_code} {assessment.status_code})")
    time.sleep(2)