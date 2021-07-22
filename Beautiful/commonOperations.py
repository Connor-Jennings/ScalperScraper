from libraries import * 

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


    def prnt(self):
        today = date.today()
        filename = str(today)+".json"
        f = open(filename, "w")
        f.write(json.dumps(self.json_array))
        f.close() 