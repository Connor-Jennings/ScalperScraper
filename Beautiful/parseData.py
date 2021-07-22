from datetime import date, timedelta
import json



def storeNewDay():
    # store data everyday for reference
    today = "./JsonFiles/" + str(date.today()) + ".json"
    f = open("./JsonFiles/newDay.json", "rt")
    w = open(today, "w")
    w.write(f.read())
    f.close() 
    w.close()


def monthlyStorage():
    # once a month store the data for reference 
    dayNumber = date.today()
    num = str(dayNumber.day)
    if num == "21":
        today = str(date.today()) + ".json"
        f = open("newDay.json", "rt")
        w = open(today, "w")
        w.write(f.read())
        f.close() 
        w.close()

def replaceOldFileWithNew():
    #update "oldDay.json" with today's data 
    f = open("./JsonFiles/newDay.json", "rt")
    w = open("./JsonFiles/oldDay.json", "w")
    w.write(f.read())
    f.close() 
    w.close()


def findNewEntries(new_data, old_data):
    new_entries = []
    i = 0 
    while i < len(new_data):
        if  new_data[i] not in old_data:
            new_entries.append(new_data[i])
        i+=1
    return new_entries


def main():
    f = open("./JsonFiles/newDay.json", "rt")
    new_data = json.load(f)
    f.close()
    f = open("./JsonFiles/oldDay.json", "rt")
    old_data = json.load(f)
    f.close()

    newEvents = findNewEntries(new_data, old_data)
    w = open("./JsonFiles/newEventsFound.json", "w")
    w.write(json.dumps(newEvents))
    
    storeNewDay()
    #monthlyStorage()
    #replaceOldFileWithNew()


if __name__ == "__main__":
    main()
    exit(0)


