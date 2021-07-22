import requests 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json

# dictionary of all pages to scrape

url = "https://www.axs.com/venues/101207/santa-barbara-bowl-santa-barbara-tickets?q=santa+barbara+bowl&cat=7"
#url = "https://www.axs.com/venues/120969/fonda-theatre-los-angeles-tickets?q=The+Fonda+Theatre+LA&cat=7"
phone_book  = {
    "Santa Barbara Bowl" : "https://www.axs.com/venues/101207/santa-barbara-bowl-santa-barbara-tickets?q=santa+barbara+bowl&cat=7",
    "Fonda Theatre" : "https://www.axs.com/venues/120969/fonda-theatre-los-angeles-tickets?q=The+Fonda+Theatre+LA&cat=7",
    "The Forum" : "https://www.axs.com/venues/101627/the-forum-inglewood-tickets?q=the+forum&cat=7",
    "The Greek Theatre LA" : "https://www.axs.com/venues/101546/the-greek-theatre-los-angeles-tickets?q=Greek+theatre&cat=7",
    "The Greek Theatre at U.C Berkeley" : "https://www.axs.com/venues/100974/the-greek-theatre-at-u-c-berkeley-berkeley-tickets?q=Greek+theatre&cat=7",
    # "Hollywood Bowl" : "https://www.axs.com/venues/101545/hollywood-bowl-hollywood-tickets?q=hollywood+bowl&cat=7" NOT ON axs
    # Neither is honda center
    "Microsoft Theater" :"https://www.axs.com/venues/101406/microsoft-theater-los-angeles-tickets?q=microsoft+theatre&cat=7",
    "The Novo" : "https://www.axs.com/venues/101912/the-novo-los-angeles-tickets?q=The+Novo&cat=7",
    "Shrine Auditorium" : "https://www.axs.com/venues/123568/shrine-auditorium-los-angeles-tickets?q=shrine+auditorium&cat=7",
    "STAPLES Center" : "https://www.axs.com/venues/101242/staples-center-los-angeles-tickets?q=staples+center&cat=7"
    # Nothing for grammy museum 
}
# create json array that will hold all of the venues and events 
json_array = []

for listing in phone_book:
    #initiating the web driver. parameter includes the path of the webdriver
    driver = webdriver.Chrome('./chromedriver')
    driver.get(phone_book[listing])  # get(url)

    #just to ensure the page is loaded
    time.sleep(5)

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

    # print what was grabbed 
    for headliner in featured_headliner1:
        headliner_array.append(str(headliner.text).strip())
        link_array.append(str(headliner['href']).strip())
        
    for headliner in featured_headliner2:
        headliner_array.append(str(headliner.text).strip())
        link_array.append(str(headliner['href']).strip())
        
    for date in featured_dates:
        broke_date = str(date.text).strip().splitlines()
        fixed_date = broke_date[0]
        date_array.append(fixed_date)
        venue_array.append(listing)
    
    for headliner in upcoming_headliners:
        headliner_array.append(str(headliner.text).strip())
        
    for date in upcoming_dates:
        date_array.append(str(date.text).strip())
        venue_array.append(listing)
        
    for link in upcoming_ticketLink:
        link_array.append(str(link['href']).strip())
        


    # create json object 
    i = 0
    
    while(i < len(headliner_array)):
        output = {}
        output['site'] = "axs"
        output["venue"] =  f"{venue_array[i]}"
        output["event"] = f"{headliner_array[i]}"
        output["status"] = ""
        output["date"] = f"{date_array[i]}"
        output["ticketLink"] =  f"{link_array[i]}" 
        json_array.append(output)
        i+=1


    # close the connection 
    driver.close() 


# output json object 
print(json.dumps(json_array))

exit(0)
