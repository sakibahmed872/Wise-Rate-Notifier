import requests
import sched, time
from datetime import datetime
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-rAUD', nargs = '?', default = '72.5')
parser.add_argument('-rUSD', nargs = '?', default = '103')
args = parser.parse_args()

URL = "https://wise.com/rates/live"
params = [{"source": "AUD", "target": "BDT"}, {"source": "USD", "target": "BDT"}]

my_scheduler = sched.scheduler(time.time, time.sleep)

def getRates():
    now = datetime.now()
    print("Current Time = ", now.strftime("%I:%M:%S %p"))

    for param in params:
        response = requests.get(URL, params=param)
        dict = response.json()
        

        print(dict["source"], "to ", dict["target"], " Rate - ",  dict["value"])

        if (dict["source"] == "AUD" and dict["value"] >= float(args.rAUD)) or (dict["source"] == "USD" and dict["value"] >= float(args.rUSD)) :
            os.system('notify-send "'+dict["source"]+' Rate High" "Current Rate is '+str(dict["value"])+' which is Higher than thresold rate"')

    
    print("\n")
    my_scheduler.enter(30, 1, getRates)
    my_scheduler.run()

if __name__ == "__main__":
    getRates()