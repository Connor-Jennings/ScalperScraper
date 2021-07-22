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


def findNewEntries(json_data):
    i=0
    for datapoint in json_data:
        i += 1
    print(i)


def main():
    f = open("./JsonFiles/newDay.json", "rt")
    json_data = json.load(f)
    f.close()

    findNewEntries(json_data)
    #storeNewDay()
    #monthlyStorage()
    #replaceOldFileWithNew()


if __name__ == "__main__":
    main()
    exit(0)


