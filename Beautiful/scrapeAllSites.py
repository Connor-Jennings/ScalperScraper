import requests 
import ticketpy
import time
import json
import re
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


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
        name = "../../JsonFiles/" + file_name
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
        u_date = re.sub("\n", "", u_date)
        u_date = re.sub("  ", "", u_date)
        u_date = re.sub("Starting", "", u_date)

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

    elif site == "novo":
        split = re.sub(',', '', u_date)
        split = re.split(" ", split)
        date = months[str(split[1])] + "/"
        if int(split[2]) < 10:
            split[2] = "0"+split[2]
        date += split[2]+"/"
        year= str(split[3])
        date += year[2] + year[3]
        return date

    elif site == "shrine":
        date = re.sub("@", "", u_date)
        date = re.sub(",", "", u_date)
        split = re.split(" ", date)
        date = months[split[1]] + "/"
        if int(split[2]) < 10:
            split[2] = "0"+split[2]
        date += split[2]+"/"
        year= str(split[3])
        date += year[2] + year[3]
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
    dates = soup.find_all('div', class_="date presented-by")

    for date in dates:
        time = date['aria-label']
        date_array.append(time)
    
    # # select link and add to array 
    # links = soup.find_all('a', class_="button-round event-list-ticket-link")                                  #### link needs work here #####

    # for link in links:
    #     link_array.append(str(link['href']).strip())
        
    # iterate through arrays and add to json object 
    i = 0
    while(i < len(date_array)):
        data.append("Venue Website", "Microsoft Theater", headliner_array[i], date_array[i], "link_array[i]")
        i+=1

    return

# Scrape The Novo by Microsoft ######################################################################################################
def novo(driver, data):
    driver.get('https://www.thenovodtla.com/events/all') 

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
    headliners = soup.find_all('h3', class_="carousel_item_title_small")

    for headliner in headliners:
        head = headliner.find('a')
        headliner_array.append(strip(head.text))

    # select date and add to array 
    dates = soup.find_all('span', class_="date")

    for date in dates:
        date = strip(date.text)
        date = format_date(date, "novo")
        date_array.append(date)


    # select link and add to array 
    links = soup.find_all('div', class_="buttons")

    for link in links:
        a = link.find('a')
        link_array.append(a['href'])
        
    # iterate through arrays and add to json object 
    i = 0
    while(i < len(headliner_array)):
        data.append("Venue Website", "The Novo by Microsoft", headliner_array[i], date_array[i], link_array[i])
        i+=1

    return 

# Scrape Shrine Auditorium ##########################################################################################################
def shrine(driver, data):
    driver.get('https://www.shrineauditorium.com/events/all') 

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
    headliners = soup.find_all('h3')

    for headliner in headliners:
        head = headliner.find('a')
        headliner_array.append(str(head.text).strip())

    # select date and add to array 
    dates = soup.find_all('h4', class_='date')

    for date in dates:
        date = format_date(strip(date.text), "shrine")
        date_array.append(date)

    # select link and add to array 
    links = soup.find_all('div',  class_="buttons span pull-right")

    for link in links:
        a = link.find_all('a')[1]
        link_array.append(a['href'])
    # iterate through arrays and add to json object 
    i = 0
    while(i < len(headliner_array)):
        data.append("Venue Website", "Shrine Auditorium", headliner_array[i], date_array[i], link_array[i])
        i+=1

    return

# Scrape STAPLES Center #############################################################################################################
def staples(driver, data):
    driver.get('https://www.staplescenter.com/events/all') 

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
        headliner_array.append(str(headliner.text).strip())
        
    # select date and add to array                                                                          ##### this date needs a bunch of work #########
    dates = soup.find_all('div', class_='date')
    for date in dates:
        date = date['aria-label']
        date_array.append(date)


    # more_info = len(driver.find_elements_by_css_selector("title.More Info"))

    # for info_num in range(1,more_info):
    #     # day = date.find('div')
    #     # date = day['aria-label']
    #     # date_array.append(date)
    #      # get the source html 

    #     # click on each more info link 
    #     # search = info.find_elements_by_tag_name('h3')
    #     driver.find_elements_by_css_selector('title.More Info')[info_num].click()
        

    #     html = driver.page_source
    #     # render all JS and stor as static html
    #     soup = BeautifulSoup(html, "html.parser")

    #     # iterate through dates and append 
    #     dates = soup.find_all('span', class_='cell')
    #     for date in dates:
    #         date = date['aria-label']
    #         date_array.append(date)

    #     driver.back()
    


    # select link and add to array 
    links = soup.find_all('div', class_='buttons')

     
    for link in links:
        try:
            a = link.find('a')['href']
            link_array.append(str(a))
        except:
            link_array.append("tbd")

    # iterate through arrays and add to json object 
    i = 0
    while(i < len(date_array)):
        data.append("Venue Website", "STAPLES Center", headliner_array[i], date_array[i], link_array[i])
        i+=1

    return

# Scrape Grammy Museum ##############################################################################################################
def grammy(driver, data):
    return 


#####################################################################################################################################
#####################################################################################################################################
#                                                  AXS and Ticketmaster                                                             #
#####################################################################################################################################

# Now find ticketmaster data ########################################################################################################
def ticketMaster(data):
    ticketmaster_phoneBook = [
        "Santa Barbara Bowl", 
        "The Fonda Theatre", 
        "The Forum Inglewood",
        "Greek Theatre Los Angeles", 
        "Greek Theatre-U.C. Berkeley",
        "Hollywood Bowl Hollywood", 
        "Honda Center", 
        "Microsoft Theater", 
        "The Novo by Microsoft", 
        "STAPLES Center"
    ]
    # my ticketmaster api
    tm_client = ticketpy.ApiClient('0ECTgjObHZdKCOMWADFoURoC6wxYIqpA')

    for listing in ticketmaster_phoneBook:

        # create arrays to fill with data 
        headliner_array = []
        date_array = []
        #status_array = []
        link_array = []

        # query ticketmaster 
        attractions = tm_client.events.find(
            keyword = str(listing)
        )

        # fill data into arrays 
        for events in attractions:
            for details in events:
                headliner_array.append(str(details.name).strip())
                date = format_date(str(details.utc_datetime).strip(), "Ticketmaster")
                date_array.append(date)
                #status_array.append(str(details.status).strip())
                link_array.append(str(details.json['url']).strip())

        # add to json object 
        i = 0
        while(i < len(headliner_array)):
            data.append("Ticketmaster", str(listing), headliner_array[i], date_array[i], link_array[i])
            i+=1
    return

# Now find axs data  #############################################################################################################        
def axs(driver, data):
    
    axs_phoneBook = {
        "Santa Barbara Bowl" : "https://www.axs.com/venues/101207/santa-barbara-bowl-santa-barbara-tickets?q=santa+barbara+bowl&cat=7",
        "The Fonda Theatre" : "https://www.axs.com/venues/120969/fonda-theatre-los-angeles-tickets?q=The+Fonda+Theatre+LA&cat=7",
        "The Forum Inglewood" : "https://www.axs.com/venues/101627/the-forum-inglewood-tickets?q=the+forum&cat=7",
        "Greek Theatre Los Angeles" : "https://www.axs.com/venues/101546/the-greek-theatre-los-angeles-tickets?q=Greek+theatre&cat=7",
        "Greek Theatre-U.C. Berkeley" : "https://www.axs.com/venues/100974/the-greek-theatre-at-u-c-berkeley-berkeley-tickets?q=Greek+theatre&cat=7",
        # "Hollywood Bowl" : "https://www.axs.com/venues/101545/hollywood-bowl-hollywood-tickets?q=hollywood+bowl&cat=7" NOT ON axs
        # Neither is honda center
        "Microsoft Theater" :"https://www.axs.com/venues/101406/microsoft-theater-los-angeles-tickets?q=microsoft+theatre&cat=7",
        "The Novo by Microsoft" : "https://www.axs.com/venues/101912/the-novo-los-angeles-tickets?q=The+Novo&cat=7",
        "Shrine Auditorium" : "https://www.axs.com/venues/123568/shrine-auditorium-los-angeles-tickets?q=shrine+auditorium&cat=7",
        "STAPLES Center" : "https://www.axs.com/venues/101242/staples-center-los-angeles-tickets?q=staples+center&cat=7"
        # Nothing for grammy museum 
    }
    
    for listing in axs_phoneBook:
        driver.get(axs_phoneBook[listing])  # get(url)

        # just to ensure the page is loaded
        # time.sleep(2.5)

        # get the source html 
        html = driver.page_source

        # this renders all the JS code and stores all 
        # of the information in static HTML code
        # Now, we can simply apply bs4 to html variable 
        soup = BeautifulSoup(html, "html.parser")


        #featured section
        featured_headliner1 = soup.select('#event-featured-section > div.c-featured-event__container > div:nth-child(1) > div.c-featured-event__info-container > div.c-featured-event__description > div > div.c-marquee.c-marquee--sm.c-event__marquee > h1 > a')
        featured_headliner2 = soup.select('#event-featured-section > div.c-featured-event__container > div:nth-child(2) > div.c-featured-event__info-container > div.c-featured-event__description > div > div.c-marquee.c-marquee--sm.c-event__marquee > h1 > a')
        featured_dates = soup.find_all('div', class_='c-featured-event__date')


        # upcoming events section 
        upcoming_headliners = soup.find_all('div', class_='headliner')
        upcoming_dates = soup.find_all('span', class_='date-wrapper')
        upcoming_ticketLink = soup.find_all('a', class_='display-table-row events_link', href=True)

        # create arrays to fill with data 
        venue_array = []
        headliner_array = []
        date_array = []
        link_array = []

        # append data to arrays
        for headliner in featured_headliner1:
            headliner_array.append(str(headliner.text).strip())
            link_array.append(str(headliner['href']).strip())
            
        for headliner in featured_headliner2:
            headliner_array.append(str(headliner.text).strip())
            link_array.append(str(headliner['href']).strip())
            
        for date in featured_dates:
            broken_date = str(date.text).strip().splitlines()
            final_date = format_date(broken_date[0], "axs")
            date_array.append(final_date)
            venue_array.append(listing)
        
        for headliner in upcoming_headliners:
            headliner_array.append(str(headliner.text).strip())
            
        for date in upcoming_dates:
            final_date = format_date(str(date.text).strip(), "axs")
            date_array.append(final_date)
            venue_array.append(listing)
            
        for link in upcoming_ticketLink:
            link_array.append(str(link['href']).strip())
            


        # add to json object 
        i = 0
        while(i < len(headliner_array)):
            data.append("axs", str(listing), headliner_array[i], date_array[i], link_array[i])
            i+=1

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
    ticketMaster(data)
    axs(driver, data)
    SB(driver, data)
    fonda(driver, data)
    forum(driver, data)
    greekLA(driver, data)
    greekBerkley(driver, data)
    hollywood(driver, data)
    honda(driver, data)
    # microsoft(driver, data)       # needs date and ticket link 
    novo(driver, data)
    shrine(driver, data)
    # staples(driver, data)        # needs date 
    # grammy(driver, data)         # check with nicole to see which site 

    # output to json file 
    data.output("newDay.json")
    # close the connection 
    driver.close() 

if __name__ == "__main__":
    main()
    exit(0)

