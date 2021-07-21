import ticketpy
import inspect
import json

# my ticketmaster api
tm_client = ticketpy.ApiClient('0ECTgjObHZdKCOMWADFoURoC6wxYIqpA')

# array of all venues to scrape
phone_book  = [
    "STAPLES Center",
    "The Novo by Microsoft", 
    "Microsoft Theater", 
    "Honda Center", 
    "Hollywood Bowl Hollywood", 
    "Greek Theatre-U.C. Berkeley", 
    "Greek Theatre Los Angeles", 
    "Santa Barbara Bowl", 
    "The Fonda Theatre", 
    "The Forum Inglewood" 
]
# create json array that will hold all of the venues and events 
json_array = []

# iterate through all of the venues 
for listing in phone_book:

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
            date_array.append(str(details.utc_datetime).strip())
            status_array.append(str(details.status).strip())
            link_array.append(str(details.json['url']).strip())
        

    # create json object 
    i = 0
    while(i < len(headliner_array)):
        output = {}
        output["site"] = "Ticketmaster"
        output["venue"] =  str(listing)
        output["event"] = f"{headliner_array[i]}"
        output["status"] = f"{status_array[i]}"
        output["date"] = f"{date_array[i]}"
        output["ticketLink"] =  f"{link_array[i]}" 
        json_array.append(output)
        i+=1


# output json object 
print(json.dumps(json_array))