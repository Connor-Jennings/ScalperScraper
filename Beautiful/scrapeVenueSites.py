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
def strip(u_name):
    name = re.sub("\n", "", u_name)
    name = re.sub("\t", "", name)
    return name

#####################################################################################################################################
def format_date(u_date,site):
    months ={
        "Jan" : "01",
        "Feb" : "02",
        "Mar" : "03",
        "Apr" : "04",
        "May" : "05",
        "Jun" : "06",
        "Jul" : "07",
        "Aug" : "08",
        "Sep" : "09",
        "Oct" : "10",
        "Nov" : "11",
        "Dec" : "12",
        "January" : "01",
        "February" : "02",
        "March" : "03",
        "April" : "04",
        "June" : "06",
        "July" : "07",
        "August" : "08",
        "September" : "09",
        "October" : "10",
        "November" : "11",
        "December" : "12",
        "Sept" : "09"
    }
    if u_date == "None":
        return u_date
    elif u_date == "TBD":
        return u_date 

    elif site == "Ticketmaster":
        split = re.split("-", u_date)
        year = int(split[0])
        month = int(split[1])
        remaining = split[2]
        split_remaining = re.split(" ", remaining)
        day = int(split_remaining[0])
        date = datetime.datetime(year, month, day)
        return str(date.strftime("%x"))
    
    elif site == "axs":
        split = re.split("-", u_date) ########## idk if this is necessary  -> go back and test this
        split = re.split(" ", u_date)

        year = split[3][2] + split[3][3]
        month = months[split[1]]
        day = re.split(",",split[2])[0] 

        return month+"/"+day+"/"+year
    
    elif site == "fonda" or site == "sbbowl":
        split = re.sub(",", "", u_date)
        split = re.split(" ", split)

        year = split[3][2] + split[3][3]
        month = months[split[1]]
        day = split[2]
        
        return month+"/"+day+"/"+year

    elif site == "forum":
        u_date = re.sub(",", "", u_date)
        split = re.split(" ", u_date)
        try:
            year = split[2][2] + split[2][3]
            date = months[split[0]] + "/"
            if int(split[1]) < 10:
                split[1] = "0"+split[1]
            date += split[1]+"/"
            date += year
            return date
        except:
            year = str(datetime.date.today().year)
            year = year[2]+year[3]
            date = months[str(split[0])] + "/"
            if int(split[1]) < 10:
                split[1] = "0"+split[1]
            date += split[1]+"/"
            date += year
            return date

    elif site == "greekla":
        split = re.sub(',', '', u_date)
        split = re.sub("  ", " ", split)
        split = re.split(" ", split)
        date = months[str(split[2])] + "/"
        if int(split[3]) < 10:
            split[3] = "0"+split[3]
        date += split[3]+"/"
        year= str(split[4])
        date += year[2] + year[3]
        return date

    elif site == 'greekberkley':
        split = re.sub(',', '', u_date)
        split = re.sub("  ", " ", split)
        split = re.split(" ", split)
        date = months[str(split[0])] + "/"
        if int(split[1]) < 10:
            split[1] = "0"+split[1]
        date += split[1]+"/"
        year= str(split[2])
        date += year[2] + year[3]
        return date

    elif site == "hollywood":
        split = re.split("-", u_date)
        date = split[1] + "/" + split[2] +"/"
        year = split[0]
        date += year[2] + year[3]
        return date
    
    elif site == "hondacenter":
        year = str(datetime.date.today().year)
        split = u_date.replace(".","")
        split = re.split(" ", split)
        date = months[split[1]] + "/"
        if int(split[2]) < 10:
            split[2] = "0"+split[2]
        date += split[2] + "/" + year[2] + year[3]
        return date

    return u_date
#####################################################################################################################################
def find_year(element):
    if hasattr(element.div.previous_sibling, "tribe-events-calendar-list__month-separator"):
        return str(element.text).strip()
    else:
        find_year(element.previous_sibling)


#####################################################################################################################################
def templateFunction(driver, data):
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
        data.append("Venue Website", "venue name", headliner_array[i], date_array[i], link_array[i])
        i+=1

    return
   

#####################################################################################################################################
#####################################################################################################################################
#                                                   Venue Functions                                                                 #
# Scrape Santa Barbara Bowl #########################################################################################################
def SB(driver, data):
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
        date_array.append(format_date(str(date).strip(), "sbbowl"))


    # select link and add to array 
    ticketLinks = soup.find_all('a', attrs={"data-event-category":"ticket_link"})
    for ticketLink in ticketLinks:
        link = ticketLink.get('href')
        link_array.append(str(link).strip())
            
    # add data to json object 
    i = 0
    while(i < len(headliner_array)):
        data.append("Venue Website", "Santa Barbara Bowl", headliner_array[i], date_array[i], link_array[i]) 
        i+=1

    return 


# Scrape The Fonda Theatre ##########################################################################################################
def fonda(driver, data):
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
        name = strip(name)
        headliner_array.append(name)


    # select date and add to array 
    dates = soup.find_all('div', class_="date-time-container")
    for date in dates:
        date = date.find('span', class_="date").text
        date = strip(date)
        date = format_date(date, "fonda")
        date_array.append(date)

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
        data.append("Venue Website", "The Fonda Theatre", headliner_array[i], date_array[i],link_array[i])
        i+=1

    return

# Scrape The Forum Inglewood ########################################################################################################
def forum(driver, data): 
    driver.get('https://thelaforum.com/events/list/') 

    # get the source html 
    html = driver.page_source
    # render all JS and stor as static html
    soup = BeautifulSoup(html, "html.parser")

    # create arrays to fill with data 
    venue_array = []
    headliner_array = []
    incomplete_dates = []
    date_array = []
    link_array = []

    # select headliner and add to array  and ticket link
    headliners = soup.find_all('a', class_='tribe-events-calendar-list__event-title-link tribe-common-anchor-thin')

    for headliner in headliners:
        headliner_array.append(str(headliner.text).strip())
        link_array.append(str(headliner['href']).strip())

    # select date and add to array 
    date = soup.find_all('span', class_="tribe-event-date-start")
    for day in date:
        day = format_date(str(day.text), 'forum')
        date_array.append(day)
   
    # # iterate through arrays and add to json object 
    i = 0
    while(i < len(headliner_array)):
        data.append("Venue Website", "The Forum Inglewood",headliner_array[i], date_array[i], link_array[i])
        i+=1

    return

# Scrape Greek Theatre Los Angeles ##################################################################################################
def greekLA(driver, data):
    driver.get('https://www.lagreektheatre.com/events/all') 

    # get the source html 
    html = driver.page_source
    # render all JS and stor as static html
    soup = BeautifulSoup(html, "html.parser")

    # create arrays to fill with data 
    venue_array = []
    headliner_array = []
    date_array = []
    link_array = []

    # select headliner and add to array and link
    headliners = soup.find_all('a', attrs={'title':'More Info'})

    for headliner in headliners:
        headliner_array.append(str(headliner.text).strip())
        link_array.append(str(headliner['href']).strip())

    # select date and add to array 
    dates = soup.find_all('span', class_="m-date__singleDate")
    
    for date in dates:
        date_array.append(format_date(str(date.text).strip(),'greekla'))

    # iterate through arrays and add to json object 
    i = 0
    while(i < len(headliner_array)):
        data.append("Venue Website", "Greek Theatre Los Angeles", headliner_array[i], date_array[i], link_array[i])
        i+=1

    return
   

# Scrape Greek Theatre-U.C. Berkeley ################################################################################################
def greekBerkley(driver, data):
    driver.get('https://thegreekberkeley.com/event-listing/') 

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
    headliners = soup.find_all('h2', class_='show-title')

    for headliner in headliners:
        headliner_array.append(str(headliner.text).strip())
        

    # select date and add to array 
    dates = soup.find_all('div', class_='date-show')
    for date in dates:
        date_array.append(format_date(str(date['content']), 'greekberkley'))


    # select link and add to array 
    links = soup.find_all('a', attrs={'target': '_blank'})
    for link in links:
        link_array.append(str(link['href']).strip())
        
    # iterate through arrays and add to json object 
    i = 0
    while(i < len(headliner_array)):
        data.append("Venue Website", "Greek Theatre-U.C. Berkeley", headliner_array[i], date_array[i], link_array[i])
        i+=1

    return
    

# Scrape Hollywood Bowl Hollywood ###################################################################################################
def hollywood(driver, data):
    driver.get('https://www.hollywoodbowl.com/events/performances?Venue=Hollywood+Bowl&Season=null') 

    # scroll down to load whole page

    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load the page.
        time.sleep(3)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height

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
    headliners = soup.find_all('span', class_="name name--short")

    for headliner in headliners:
        head = strip(str(headliner.text).strip())
        while "  " in head:
            head = re.sub("  ", " ", head)
        headliner_array.append(head)

    # select date and add to array 
    dates = soup.find_all('div', class_="performance-card__anchor")
    for date in dates:
        day = date['data-day']
        day = format_date(day, "hollywood")
        date_array.append(day)


    # select link and add to array 
    links = soup.find_all('a', class_="btn performance-buy-btn")
    for link in links:
        link_array.append(str(link['href']).strip())

    # iterate through arrays and add to json object 
    i = 0
    while(i < len(link_array)):
        data.append("Venue Website", "Hollywood Bowl Hollywood", headliner_array[i], date_array[i], link_array[i])
        i+=1

    return
   

# Scrape Honda Center ###############################################################################################################
def honda(driver, data):
    driver.get('https://www.hondacenter.com/events/') 

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
    headliners = soup.find_all('h2', class_='event-list-name')

    for headliner in headliners:
        headliner_array.append(str(headliner.text).strip())

    # select date and add to array 
    dates = soup.find_all('div', class_="event-list-time")

    for date in dates:
        date = format_date(str(date.text).strip(), "hondacenter")
        date_array.append(date)
    
    # select link and add to array 
    links = soup.find_all('a', class_="button-round event-list-ticket-link")

    for link in links:
        link_array.append(str(link['href']).strip())
        
    # iterate through arrays and add to json object 
    i = 0
    while(i < len(headliner_array)):
        data.append("Venue Website", "Honda Center", headliner_array[i], date_array[i], link_array[i])
        i+=1

    return
   

# Scrape Microsoft Theater ##########################################################################################################
def microsoft(driver, data):
    driver.get('https://www.microsofttheater.com/events/all') 

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
    headliners = soup.find_all('h3', class_='title')

    for headliner in headliners:
        name = headliner.find('a')
        headliner_array.append(name.text)

    # select date and add to array 
    dates = soup.find_all('div', class_="info clearfix")

    for date in dates:
        time = date.find('div', class_='date presented-by')
        date = time['aria-label']
        print(date)
        date_array.append(date)
    
    # # select link and add to array 
    # links = soup.find_all('a', class_="button-round event-list-ticket-link")

    # for link in links:
    #     link_array.append(str(link['href']).strip())
        
    # iterate through arrays and add to json object 
    i = 0
    while(i < len(headliner_array)):
        data.append("Venue Website", "Microsoft Theater", headliner_array[i], date_array[i], "link_array[i]")
        i+=1

    return

# Scrape The Novo by Microsoft ######################################################################################################
def novo(driver, data):
    return 

# Scrape Shrine Auditorium ##########################################################################################################
def shrine(driver, data):
    return 

# Scrape STAPLES Center #############################################################################################################
def staples(driver, data):
    return 

# Scrape Grammy Museum ##############################################################################################################
def grammy(driver, data):
    return 

#####################################################################################################################################
#####################################################################################################################################
#                                                   Main                                                                            #
#####################################################################################################################################

def main():
    # create json instance 
    global data
    data = JsonInstance([])

    global driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome('./chromedriver', options=chrome_options)
    
    # collect data from each website 
    # SB(driver, data)
    # fonda(driver, data)
    # forum(driver, data)
    # greekLA(driver, data)
    # greekBerkley(driver, data)
    # hollywood(driver, data)
    # honda(driver, data)
    microsoft(driver, data)
    # novo(driver, data)
    # shrine(driver, data)
    # staples(driver, data)
    # grammy(driver, data)

    # output to json file 
    data.output("venueSitesData.json")
    # close the connection 
    driver.close() 

if __name__ == "__main__":
    main()
    exit(0)

