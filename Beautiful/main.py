import os
import smtplib
from email.message import EmailMessage
import subprocess
import json

def mail():

    w = open("./JsonFiles/newEventsFound.json", "rt")
    newEvents = json.load(w)
    body = "New Events Posted \n\n"
    for event in newEvents:
        body += event['event'] + "\n"
        body += "  ---------------------------------\n"
        body += "\tvenue: " + event['venue'] + "\n"
        body += "\tdate: " + event['date'] + "\n"
        body += "\twebsite: " + event['site'] + "\n"
        body += "\tticketLink: " + event['ticketLink'] + "\n\n\n"



    gmail_user = 'connorwork123321@gmail.com'
    gmail_password = '6711Connor'

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = 'Tickets'
    msg['From'] = gmail_user
    msg['To'] = ["jennings.co.d@gmail.com"]



    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.send_message(msg)
        server.quit()

        print ('Email sent!')

    except:
        print ('Something went wrong...')





def main():
    # os.system("python3 alltogethernow.py")
    os.system("python3 parseData.py")
    mail()

if __name__ == "__main__":
    main()
    exit(0)