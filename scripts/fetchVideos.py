import requests
import json
import sys
import os
from pathlib import Path
home = str(Path.home())


os.system("mkdir -p $HOME/videoJson/")
size = 100
inp = sys.argv
if len(inp)==3:
    api_token=inp[1]
    size = inp[2]
elif len(inp)==2:
    api_token = inp[1]
else:
    print("please input in format -> python script.py 'token'")
    exit()

url="https://www.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics%2CtopicDetails&chart=mostPopular&pageToken=&regionCode=US&key="+api_token
#url ="https://www.googleapis.com/youtube/v3/videos?part=snippet%2Cstatistics&chart=mostPopular&pageToken=&regionCode=US&key="+api_token

mylist = []
mycounts = {}
totalcount = (int(size)/5)%200
data ={}
while(totalcount>0):
    r = requests.get(url,headers={"Content-Type": "application/json"})
    jsonObj  = r.json()
    if (r.status_code==200  or r.status_code == 304) and (len(jsonObj)!=0):
        for i in jsonObj["items"]:
            if i["contentDetails"]["caption"] == "true":        ## compute only if capions are present
                data['id'] = i["id"]
                data['title'] = i["snippet"]["title"]
                data['publishedAt'] = i["snippet"]["publishedAt"]
                data['channelTitle'] = i["statistics"]["channelTitle"]
                data['categoryId'] = i["snippet"]["categoryId"]
                if 'tags' in i["snippet"]:
                    data['tags'] = i["snippet"]["tags"]
                data['statistics'] = i["statistics"]
                if 'topicDetails' in i:
                    data['topicDetails'] = i["topicDetails"]
                with open(home+'/videoJson/'+i["id"]+'.json', 'w') as outfile:
                    json.dump(data, outfile)
                os.system("./extractor.sh "+i["id"])
    else:
        break
    if 'nextPageToken' not in jsonObj:
        break
    url = "https://www.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics%2CtopicDetails&chart=mostPopular&pageToken=" + \
          jsonObj["nextPageToken"] + "&regionCode=US&key=" + api_token
    totalcount=totalcount-1
