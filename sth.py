import json
import requests
from firebase import firebase
import datetime

ROUTES=19

firebase = firebase.FirebaseApplication("https://route-32.firebaseio.com/", None)

checked=[set() for i in range(ROUTES)]
times=[{} for j in range(ROUTES)]

# db=shelve.open("base")
def makeunix(st_time):
    time_correctly = st_time.split()[1]
    return time_correctly

def time_maker(a="11:54:04"):
    hour = int(a[0:-6])
    min_ = int(a[3:-3])
    sec = int(a[6:])
    time = int(hour*3600 + min_*60 + sec)
    return time


while True:
    try:
        # print("ok")
        response = requests.get("http://map.ettu.ru/api/v2/troll/boards/?apiKey=111&order=1").text
        data = json.loads(response)["vehicles"]
        for information in data:
            if information["ROUTE"] in ["3","1","5","7","9","11","17","18"]:
                lat = float(information["LAT"])
                lon = float(information["LON"])
                if 56.847254<=lat<=56.849504 and 60.606693<=lon<=60.609291:
                    board = information["BOARD_ID"]
                    course = information["COURSE"]
                    need = '{"gps":{"lat":' + str(lat) + ', "lon":' + str(lon) + '}, "course":' + course + "}"
                    good_time=str(makeunix(information["ATIME"]))
                    if good_time not in checked[int(information["ROUTE"])]:
                        print(information["ROUTE"],good_time, need)
                        push = firebase.put("https://route-32.firebaseio.com/all/" +information["ROUTE"]+"/" + board + "/",
                                            good_time, need)
                        checked[int(information["ROUTE"])].add(good_time)
                        times[int(information["ROUTE"])][good_time]=time_maker(good_time)
                    else:
                        for bad_time in checked[int(information["ROUTE"])]:
                            if time_maker(str(datetime.datetime.now())[11:19])+7200-int(bad_time)>=300:
                                checked[int(information["ROUTE"])].remove(bad_time)
            elif information["ROUTE"]=="4":
                lat = float(information["LAT"])
                lon = float(information["LON"])
                # if 56.84758733<=lat<=56.84796284 and 60.60792446<=lon<=60.61104655:
                if 56.84739665<=lat<=56.84818872 and 60.60792446<=lon<=60.61109215:
                    board = information["BOARD_ID"]
                    course = information["COURSE"]
                    need = '{"gps":{"lat":' + str(lat) + ', "lon":' + str(lon) + '}, "course":' + course + "}"
                    good_time=str(makeunix(information["ATIME"]))
                    if good_time not in checked[int(information["ROUTE"])]:
                        print(information["ROUTE"],good_time, need)
                        push = firebase.put("https://route-32.firebaseio.com/all/" +information["ROUTE"]+"/" + board + "/",
                                            good_time, need)
                        checked[int(information["ROUTE"])].add(good_time)
                        times[int(information["ROUTE"])][good_time]=time_maker(good_time)
                    else:
                        for bad_time in checked[int(information["ROUTE"])]:
                            if time_maker(str(datetime.datetime.now())[11:19])+7200-int(bad_time)>=300:
                                checked[int(information["ROUTE"])].remove(bad_time)


    except:
        pass
