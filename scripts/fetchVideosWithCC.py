import requests
import json
import sys
import os
from pathlib import Path
home = str(Path.home())


os.system("mkdir -p $HOME/videoJson/")
size = 10000
inp = sys.argv
if len(inp)==3:
    api_token=inp[1]
    size = inp[2]
elif len(inp)==2:
    api_token = inp[1]
else:
    print("please input in format -> python script.py 'token'")
    exit()

outerurl="https://www.googleapis.com/youtube/v3/search?key="+api_token+"&q=america&part=id&type=video&videoCaption=closedCaption&regionCode=US"
innerurl="https://www.googleapis.com/youtube/v3/videos?id=Ks-_Mh1QhMc,c0KYU2j0TM4,eIho2S0ZahI&part=snippet,contentDetails,statistics,topicDetails&regionCode=US&key=APIKEY"

mylist = []
mycounts = {}
totalcount = (int(size)/5)
data ={}
while(totalcount>0):
    r = requests.get(outerurl,headers={"Content-Type": "application/json"})
    jsonObj  = r.json()
    videoIds = ""
    if (r.status_code==200  or r.status_code == 304) and (len(jsonObj)!=0):
        for i in jsonObj["items"]:
            if 'videoId' in i["id"]:
                videoIds += i["id"]["videoId"] +","
        
        videoIds = videoIds[0:len(videoIds)-1]
        # request for video content
        innerurl="https://www.googleapis.com/youtube/v3/videos?id="+videoIds+"&part=snippet,contentDetails,statistics,topicDetails&regionCode=US&key="+api_token
        vr = requests.get(innerurl,headers={"Content-Type": "application/json"})
        videojsonObj = vr.json()
        if (vr.status_code==200  or vr.status_code == 304) and (len(videojsonObj)!=0):
            for i in videojsonObj["items"]:
                data['id'] = i["id"]
                data['title'] = i["snippet"]["title"]
                data['publishedAt'] = i["snippet"]["publishedAt"]
                data['channelTitle'] = i["snippet"]["channelTitle"]
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
    outerurl = outerurl="https://www.googleapis.com/youtube/v3/search?key="+api_token+"&part=id&type=video&videoCaption=closedCaption&pageToken=" + \
          jsonObj["nextPageToken"] + "&regionCode=US"
    totalcount=totalcount-1
    print(totalcount)
