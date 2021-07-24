import requests 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import json
import re
import datetime
#####################################################################################################################################
#####################################################################################################################################
#                                             Useful Functions & Classes                                                            #                 
#####################################################################################################################################
# singleton class to build json object ##############################################################################################
class JsonInstance:
    json_array = []

    def __init__(self, json_array):
        self.json_array = json_array

    def append(self, site, venue, event, date, ticketLink):
        output = {}
        output["site"] = site
        output["venue"] =  venue
        output["event"] = event
        output["date"] = date
        output["ticketLink"] =  ticketLink 
        self.json_array.append(output)


    def output(self, file_name):
        name = "./JsonFiles/" + file_name
        f = open(name, "w")
        f.write(json.dumps(self.json_array))
        f.close() 
#####################################################################################################################################
def find_by_label(soup, tag,  label):
    return soup.find(tag, text=re.compile(label)).next_sibling

#####################################################################################################################################
def name_strip(u_name):
    u_name = re.sub("\n", "", u_name)
    u_name = re.sub("\t", "", u_name)
    return u_name


#####################################################################################################################################
def templateFunction(data):
    # initiating the web driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome('./chromedriver', options=chrome_options)
    driver.get('https://website.com') 

    # get the source html 
    html = driver.page_source
    # render all JS and stor as static html
    soup = BeautifulSoup(html, "html.parser")

    # create arrays to fill with data 
    venue_array = []
    headliner_array = []
    date_array = []
    link_array = []

    # select headliner and add to array 
    headliners = soup.find_all('element', class_='headliner')
    featured_headliner1 = soup.select('XPath')

    for headliner in headliners:
        headliner_array.append(str(headliner.text).strip())
        link_array.append(str(headliner['href']).strip())

    # select date and add to array 

    # select link and add to array 
        
    # iterate through arrays and add to json object 
    i = 0
    while(i < len(headliner_array)):
        data.append("Venue Site", "www.venue.com", headliner_array[i], date_array[i], link_array[i])
        i+=1

    # close the connection 
    driver.close() 
    return
   

#####################################################################################################################################
#####################################################################################################################################
#                                                   Venue Functions                                                                 #
# Scrape Santa Barbara Bowl #########################################################################################################
def SB(data):
     # initiating the web driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome('./chromedriver', options=chrome_options)
    driver.get('https://sbbowl.com/concerts') 

    # get the source html 
    html = driver.page_source
    # render all JS and stor as static html
    soup = BeautifulSoup(html, "html.parser")

    # create arrays to fill with data 
    venue_array = []
    headliner_array = []
    date_array = []
    link_array = []

    # select headliner and add to array 
    headliners = soup.find_all('h3', class_='announceTitle')
    for headliner in headliners:
        name = headliner.find('a')
        headliner_array.append(str(name.text).strip())

    # select date and add to array 
    date_parents = soup.find_all('div', class_='span7 concertEmbedDeets')
    for date_parent in date_parents: 
        date = find_by_label(date_parent,'span', 'Date:')
        date_array.append(str(date).strip())


    # select link and add to array 
    ticketLinks = soup.find_all('a', attrs={"data-event-category":"ticket_link"})
    for ticketLink in ticketLinks:
        link = ticketLink.get('href')
        link_array.append(str(link).strip())
            
    # add data to json object 
    i = 0
    while(i < len(headliner_array)):
        data.append("Venue Site", "Santa Barbara Bowl", headliner_array[i], date_array[i], link_array[i]) 
        i+=1

    # close the connection 
    driver.close() 
    return 


# Scrape The Fonda Theatre ##########################################################################################################
def fonda(data):
    # initiating the web driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome('./chromedriver', options=chrome_options)
    driver.get('https://www.fondatheatre.com/events/all') 

    # get the source html 
    html = driver.page_source
    # render all JS and stor as static html
    soup = BeautifulSoup(html, "html.parser")

    # create arrays to fill with data 
    venue_array = []
    headliner_array = []
    date_array = []
    link_array = []

    # select headliner and add to array 
    headliners = soup.find_all('h3', attrs={"class": "carousel_item_title_small"})
    for headliner in headliners:
        name = headliner.find('a').text
        name.get('')
        name = name.encode('utf8')
        name = str(name).strip()
        name = name_strip(name)
        headliner_array.append(name)


    # select date and add to array 
    # dates = soup.find_all('span', class_="date")
    # for date in dates:
    #     date = date.find('span')
    #     print(date)
        # date = find_by_label(date,'span', '::before')
        # date_string = date_string.text
        # date_string = name.encode('utf8')
        # date_string = str(date_string).strip()
        # date_array.append(name)

    # select link and add to array 
    ticketLinks = soup.find_all('div', class_='buttons')
    # ticketLinks = soup.find_all('a', class_="btn-tickets accentBackground widgetBorderColor secondaryColor tickets status_1")
    for ticketLink in ticketLinks:
        link = ticketLink.find('a')
        link = link.get('href')
        link_array.append(str(link).strip())
        
    # iterate through arrays and add to json object 
    i = 0
    while(i < len(headliner_array)):
        data.append("Venue Site", "The Fonda Theatre", headliner_array[i], "date_array[i]",link_array[i])
        i+=1

    # close the connection 
    driver.close() 
    return

# Scrape The Forum Inglewood ########################################################################################################
def forum(data): 
    return 

# Scrape Greek Theatre Los Angeles ##################################################################################################
def greekLA(data):
    return 

# Scrape Greek Theatre-U.C. Berkeley ################################################################################################
def greekBerkley(data):
    return 

# Scrape Hollywood Bowl Hollywood ###################################################################################################
def hollywood(data):
    return 

# Scrape Honda Center ###############################################################################################################
def honda(data):
    return

# Scrape Microsoft Theater ##########################################################################################################
def microsoft(data):
    return

# Scrape The Novo by Microsoft ######################################################################################################
def novo(data):
    return 

# Scrape Shrine Auditorium ##########################################################################################################
def shrine(data):
    return 

# Scrape STAPLES Center #############################################################################################################
def staples(data):
    return 

# Scrape Grammy Museum ##############################################################################################################
def grammy(data):
    return 

#####################################################################################################################################
#####################################################################################################################################
#                                                   Main                                                                            #
#####################################################################################################################################

def main():
    # create json instance 
    global data
    data = JsonInstance([])
    
    # collect data from each website 
    #SB(data)
    fonda(data)
    forum(data)
    greekLA(data)
    greekBerkley(data)
    hollywood(data)
    honda(data)
    microsoft(data)
    novo(data)
    shrine(data)
    staples(data)
    grammy(data)

    # output to json file 
    data.output("venueSitesData.json")

if __name__ == "__main__":
    main()
    exit(0)

