import os
import sys
import smtplib, ssl
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.application import MIMEApplication
import json
import csv

import time
from datetime import datetime

import requests 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options



#####################################################################################################################################
#####################################################################################################################################

def mail(email_address, error):
    # username and password for gmail 
    gmail =  'ticketbot98@gmail.com'
    password = 'saladsareascam'

    # Create email object
    message = MIMEMultipart('mixed')
    message['From'] = 'Ticket Bot <{sender}>'.format(sender = gmail)
    message['To'] = email_address 
    # message['CC'] = 'contact@company.com'
    message['Subject'] = 'Tickets'


    # open json file and parse data for email body 
    w = open("/Users/connorjennings/Code/ScalperScraper/Beautiful/JsonFiles/newEventsFound.json", "rt")
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
        if(error == False):
            body = MIMEText(msg_content)
        elif(error == True):
            body = MIMEText("error")
        message.attach(body)

        ####### attach files #####
        # # attach json file 
        attachmentPath = "/Users/connorjennings/Code/ScalperScraper/Beautiful/JsonFiles/newDay.json"
        try:
            with open(attachmentPath, "rb") as attachment:
                p = MIMEApplication(attachment.read(),_subtype="json")	
                p.add_header('Content-Disposition', "attachment; filename= %s" % attachmentPath.split("\\")[-1]) 
                message.attach(p)
        except Exception as e:
            print(str(e))

        # create cvs file
        with open('/Users/connorjennings/Code/ScalperScraper/Beautiful/JsonFiles/newDay.json') as json_file:
            jsondata = json.load(json_file)
        
        data_file = open('/Users/connorjennings/Code/ScalperScraper/Beautiful/JsonFiles/newDay.csv', 'w', newline='')
        csv_writer = csv.writer(data_file)
        
        count = 0
        for data in jsondata:
            if count == 0:
                header = data.keys()
                csv_writer.writerow(header)
                count += 1
            csv_writer.writerow(data.values())
        
        data_file.close()
        attachmentPath = "/Users/connorjennings/Code/ScalperScraper/Beautiful/JsonFiles/newDay.cvs"
        # attach csv file 
        with open("/Users/connorjennings/Code/ScalperScraper/Beautiful/JsonFiles/newDay.csv", "rb") as attachment:
            p = MIMEApplication(attachment.read(),_subtype="csv")	
            p.add_header('Content-Disposition', "attachment; filename= %s" % attachmentPath.split("\\")[-1]) 
            message.attach(p)
        ###########################
       

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
            server.sendmail(gmail, email_address, msg_full)
            server.quit()

        print("Email sent to : " + email_address)
    else:
        print("No changes to send")


#####################################################################################################################################
def getemails():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome('/Users/connorjennings/Code/ScalperScraper/Beautiful/chromedriver', options=chrome_options)
    
    driver.get('https://www.saladsareascam.com/wp-admin/users.php') 

    # log into site
    username = driver.find_element_by_id("user_login")
    password = driver.find_element_by_id("user_pass")
    username.send_keys("user")
    password.send_keys("FJS3hgDG2Abv")
    response = driver.find_element_by_id("wp-submit").click()

    # get the source html 
    html = driver.page_source
    # render all JS and stor as static html
    soup = BeautifulSoup(html, "html.parser")
    
    # grab all the emails
    email_array = []
    container = soup.find_all('td', class_="email column-email")
    for item in container:
        email = str(item.find('a').text)
        email_array.append(email)
    return email_array



#####################################################################################################################################
#                                                     Main                                                                          #
#####################################################################################################################################


def main():
    argv = sys.argv[1:]
    recipients = ["jennings.co.d@gmail.com"] # getemails()

    # help command
    if "h" in argv:
        option = "\nOptions : \n \t  runforever - run on a continuous loop forever      \n \t  a - run everything     \n \t  s - only scrape    \n \t  p - only parse  \n \t \t y - dont relplace old file (can pass this in 'a' too) \n \t  m - only send mail \n "
        print(option)
        return 

    # run forever
    elif "runforever" in argv:
        while True:
            now = datetime.now()
            dt_string = now.strftime("%H")
            if dt_string == "04":
                while True:
                    try:
                        os.system("python3 /Users/connorjennings/Code/ScalperScraper/Beautiful/scrapeAllSites.py")
                        os.system("python3 /Users/connorjennings/Code/ScalperScraper/Beautiful/parseData.py") 
                        for x in recipients:
                            mail(x, False)
                        # sleep for one day 
                        time.sleep(86400)
                    except:
                        mail("jennings.co.d@gmail.com", True)
                        return
            else: 
                # sleep for one hour 
                time.sleep(3600)
        
        
    # run all systems  
    elif "a" in argv:
        try:
            os.system("python3 /Users/connorjennings/Code/ScalperScraper/Beautiful/scrapeAllSites.py")
            if "y" in argv : # if y in then dont replace oldDay
                os.system("python3 /Users/connorjennings/Code/ScalperScraper/Beautiful/parseData.py y")
            else:
                os.system("python3 /Users/connorjennings/Code/ScalperScraper/Beautiful/parseData.py") 
            for x in recipients:
                mail(x, False)
        except:
            mail("jennings.co.d@gmail.com", True)
        return

    # only parse 
    elif "p" in argv:
        if "y" in argv :
            os.system("python3 /Users/connorjennings/Code/ScalperScraper/Beautiful/parseData.py y")
        else:
            os.system("python3 /Users/connorjennings/Code/ScalperScraper/Beautiful/parseData.py")
        return  

    # only send mail
    elif "m" in argv:
        for x in recipients:
            mail(x, False)
        return    

    # only run scrape program
    elif "s" in argv:
        os.system("python3 /Users/connorjennings/Code/ScalperScraper/Beautiful/scrapeAllSites.py")
        return 
    
    print("No arguments passed... (for help) Try -> python3 main.py h ")



if __name__ == "__main__":
    main()
    exit(0)