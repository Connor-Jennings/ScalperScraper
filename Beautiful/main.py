import os
import sys
import smtplib, ssl
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.application import MIMEApplication
import json

def mail(email_address):
    # username and password for gmail 
    gmail =  'connorwork123321@gmail.com'
    password = '6711Connor'

    # Create email object
    message = MIMEMultipart('mixed')
    message['From'] = 'Ticket Bot <{sender}>'.format(sender = gmail)
    message['To'] = email_address 
    # message['CC'] = 'contact@company.com'
    message['Subject'] = 'Tickets'


    # open json file and parse data for email body 
    w = open("./JsonFiles/newEventsFound.json", "rt")
    newEvents = json.load(w)
    msg_content = "Events added or changed : \n\n"
    if len(newEvents) > 0 :
        for event in newEvents:
            msg_content += event['event'] + "\n"
            msg_content += "  ---------------------------------\n"
            msg_content += "\tvenue: " + event['venue'] + "\n"
            msg_content += "\tdate: " + event['date'] + "\n"
            msg_content += "\twebsite: " + event['site'] + "\n"
            msg_content += "\tticketLink: " + event['ticketLink'] + "\n\n\n"

        # attach email body 
        body = MIMEText(msg_content)
        message.attach(body)

        # attach file 
        attachmentPath = "./JsonFiles/newDay.json"
        try:
            with open(attachmentPath, "rb") as attachment:
                p = MIMEApplication(attachment.read(),_subtype="json")	
                p.add_header('Content-Disposition', "attachment; filename= %s" % attachmentPath.split("\\")[-1]) 
                message.attach(p)
        except Exception as e:
            print(str(e))

        # convert message to string 
        msg_full = message.as_string()

        # initiate the TLS context and use it to communicate with SMTP server.
        context = ssl.create_default_context()

        # Initialize the connection with SMTP server and set the TLS context, then start the handshaking process.
        # Next it authenticate our gmail account, and in the send mail method, you can specify the sender, 
        # to and cc (as a list), as well as the message string. (cc is optional)
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()  
            server.starttls(context=context)
            server.ehlo()
            server.login(gmail, password)
            server.sendmail(gmail, "jennings.co.d@gmail.com", msg_full)
            server.quit()

        print("Email sent!")
    else:
        print("No changes to send")



def main():
    argv = sys.argv[1:]
    recipients = ['jennings.co.d@gmail.com']

    # help command
    if "h" in argv:
        option = "\nOptions :  \n \t  a - run everything               \n \t  s - only scrape    \n \t  p - only parse  \n \t \t y - dont relplace old file (can pass this in 'a' too) \n \t  m - only send mail \n "
        print(option)
        return 

    # run all systems  
    elif "a" in argv:
        os.system("python3 scrapeAllSites.py")
        if "y" in argv : # if y in then dont replace oldDay
            os.system("python3 parseData.py y")
        else:
            os.system("python3 parseData.py")
        for x in recipients:
            mail(x)

    # only parse 
    elif "p" in argv:
        if "y" in argv :
            os.system("python3 parseData.py y")
        else:
            os.system("python3 parseData.py")
        return  

    # only send mail
    elif "m" in argv:
        recipients = ['jennings.co.d@gmail.com']
        for x in recipients:
            mail(x)
        return    

    # only run scrape program
    elif "s" in argv:
        os.system("python3 scrapeAllSites.py")
        return 
    
    print("No arguments passed... (for help) Try -> python3 main.py h ")



if __name__ == "__main__":
    main()
    exit(0)