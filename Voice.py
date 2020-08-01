from __future__ import print_function
import os
import time
import speech_recognition as sr
import pyttsx3
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
import pytz
import subprocess
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
months=["january","february",'march','april','may','june','july','august','september','october','november','december']
abb=["jan",'feb']
days=['monday','tuesday','wednesday','thursday','friday','saturday',"sunday"]
number=[str(i) for i in range(1,32)]
years=[str(k) for k in range(2021,2121)]
def speak(text):
   engine=pyttsx3.init()
   engine.say(text)
   engine.runAndWait()


def get_voice():
    voice=sr.Recognizer()
    with sr.Microphone() as source:
        audio=voice.listen(source)
        spoken=''
        try:
            spoken=voice.recognize_google(audio)
        except Exception as e:
            return "EXCEPTION"
        return spoken.lower()



def notepad(text):
    name=datetime.datetime.now()
    file_name=str(name).replace(':','_')+'-note.txt'
    with open(file_name,'w') as f:
        f.write(text)
    subprocess.Popen(['notepad.exe',file_name])



def authenticate():
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

    service = build('calendar', 'v3', credentials=creds)
    return service


def apicall(day_date,service):
    # Call the Calendar API
    date=datetime.datetime.combine(day_date,datetime.datetime.min.time())
    end_date=datetime.datetime.combine(day_date,datetime.datetime.max.time())
    utc=pytz.UTC
    date=date.astimezone(utc)
    end_date=end_date.astimezone(utc)
    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(),
                                         timeMax=end_date.isoformat(),singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak('No upcoming events found.')
    else:

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            time=str(start.split('T')[1].split('-')[0])
            if int(time.split(':')[0])<12:
                time=time.split(':')[0]+time.split(':')[1]+'am'
            else:
                time=str(int(time.split(':')[0])-12)+time.split(':')[1]+'pm'
            speak(event["summary"]+'at'+time)

   

def get_date(text):
    text=text.lower()
    today=datetime.date.today()
    month=-1
    day=-1
    year=-1
    num=-1
    if text.count("today")>0:
        return today
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    if text.count("tomorrow") > 0:
        return tomorrow

    rep=text.split(' ')
    for w in rep:
        if w in months:
            month=months.index(w)+1
        elif w in days:
            day=days.index(w)
        elif w in number:
            num=int(w)
        elif w in years:
            year=int(w)
        else:
            if 'st' in w or 'rd' in w or 'nd' in w or 'th' in w:
                    n=''
                    for i in range(len(w)):
                        if w[i] in '123456789':
                            n=n+w[i]
                    if n!='':
                        num=int(n)
        if num!=-1 and month!=-1 and year!=-1:
            break
    
    if num!=-1 and  month>=today.month :
        if year==-1:
            year=today.year

        return datetime.date(month=month,day=num,year=year)
    if month<today.month and month!=-1 and day==-1 and year==-1 and num==-1:
        year=today.year+1
        num=int(w[-2])
    if month<today.month and month!=-1 and day==-1 and year==-1 and num!=-1:
        year=today.year+1
    if month==-1 and num<today.day and year==-1 and day==-1:
        month=today.month
        year=today.year
    if day!=-1 and month==-1 and year==-1 and num==-1:
        current_weekday=datetime.datetime.today().weekday()
        if day>=current_weekday:
            num=today.day+abs(current_weekday-day)
        else:
            num=today.day+7+(day-current_weekday)
        month=today.month
        year=today.year
    if year==-1:
        year=today.year
    if month==-1:
        month=today.month
    return datetime.date(month=month,day=num,year=year)
  
      
    


service=authenticate()
password='256 albaqara'
speak("say the password to initiate your program")
print("OKAY")
response=get_voice()
while response==password:
    speak("password correct please start speaking ")
    flag=0
    text=get_voice()
    calendar=["open calendar",'calendar','meetings','classes','google']
    
    for keys in calendar:
        if keys in text:
            speak("Your calendar is at your service")
            text=get_voice()
            apicall(get_date(text),service)
            flag=-1
            break
    if flag==0:
        note=['notes','open notes','write','read','files']
        for keys in note:
            if keys in note:
                speak("notepad is deployed start speaking")
                text=get_voice()
                notepad(text)
                flag=-1
                break
    if flag==0:
        speak("i did not understand")



        






