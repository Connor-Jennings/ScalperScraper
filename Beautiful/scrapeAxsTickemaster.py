# for axs portion 
import requests 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
# for ticketmaster 
import ticketpy
# for both 
import json
import re
import datetime



# singleton class to build json object 
class JsonInstance:
    json_array = []

    def __init__(self, json_array):
        self.json_array = json_array

    def append(self, site, venue, event, status, date, ticketLink):
        output = {}
        output["site"] = site
        output["venue"] =  venue
        output["event"] = event
        output["status"] = status
        output["date"] = date
        output["ticketLink"] =  ticketLink 
        self.json_array.append(output)


    def output(self):
        f = open("./JsonFiles/newDay.json", "w")
        f.write(json.dumps(self.json_array))
        f.close() 

# for better formatting the axs dates
def date_strip(date):
    date = re.sub("\n", "", date)
    date = re.sub("  ", "", date)
    date = re.sub("Starting", "", date)
    return date

# put the dates into a standard format
def format_date(u_date,site):
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
        split = re.split("-", u_date)
        split = re.split(" ", u_date)
        
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
            "Dec" : "12"
        }

        year = split[3][2] + split[3][3]
        month = months[split[1]]
        day = re.split(",",split[2])[0] 

        return month+"/"+day+"/"+year



def main():
    # lets define our phone books 
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

    # create json class 
    data = JsonInstance([])


    # Now find ticketmaster data ###############################################################################################

    # my ticketmaster api
    tm_client = ticketpy.ApiClient('0ECTgjObHZdKCOMWADFoURoC6wxYIqpA')

    for listing in ticketmaster_phoneBook:

        # create arrays to fill with data 
        headliner_array = []
        date_array = []
        status_array = []
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
                status_array.append(str(details.status).strip())
                link_array.append(str(details.json['url']).strip())

        # add to json object 
        i = 0
        while(i < len(headliner_array)):
            data.append("Ticketmaster", str(listing), headliner_array[i], status_array[i], date_array[i], link_array[i])
            i+=1

        

    # Now find axs data  #####################################################################################################

    for listing in axs_phoneBook:
        # initiating the web driver
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome('./chromedriver', options=chrome_options)
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
            broke_date = str(date.text).strip().splitlines()
            fixed_date = date_strip(broke_date[0])
            final_date = format_date(fixed_date, "axs")
            date_array.append(final_date)
            venue_array.append(listing)
        
        for headliner in upcoming_headliners:
            headliner_array.append(str(headliner.text).strip())
            
        for date in upcoming_dates:
            final_date = format_date(date_strip(str(date.text).strip()), "axs")
            date_array.append(final_date)
            venue_array.append(listing)
            
        for link in upcoming_ticketLink:
            link_array.append(str(link['href']).strip())
            


        # add to json object 
        i = 0
        while(i < len(headliner_array)):
            data.append("axs", str(listing), headliner_array[i], "n/a", date_array[i], link_array[i])
            i+=1



        # close the connection 
        driver.close() 


    # finally output json object 
    data.output()



if __name__ == "__main__":
    main()
    exit(0)