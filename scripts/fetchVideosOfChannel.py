import requests
import json
import sys
import os
from pathlib import Path
home = str(Path.home())


os.system("mkdir -p $HOME/videoJson/")
size = 100
inp = sys.argv
if len(inp)==4:
    api_token=inp[1]
    channel = inp[2]
    size = inp[3]
elif len(inp)==3:
    api_token = inp[1]
    channel = inp[2]
else:
    print("please input in format -> python script.py 'token' 'channel_id' '{optional - size}'")
    print("example channel - UCsT0YIqwnpJCM-mx7-gSA4Q")
    exit()

######
# - videos details - https://www.googleapis.com/youtube/v3/videos?id=Ks-_Mh1QhMc,c0KYU2j0TM4,eIho2S0ZahI&part=snippet,contentDetails,statistics,topicDetails&regionCode=US&key=APIKEY
# channel - https://www.youtube.com/channel/UCsT0YIqwnpJCM-mx7-gSA4Q
# search - https://www.googleapis.com/youtube/v3/search?key=APIKEY&channelId=UCsT0YIqwnpJCM-mx7-gSA4Q&part=snippet,id&order=date&maxResults=50
# api doc - https://developers.google.com/youtube/v3/docs/videos/list
# videos part popular - https://www.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics%2CtopicDetails&chart=mostPopular&pageToken=&regionCode=US&key=APIKEY
#####


# first fetch videos from channel, pull the id of video and later do get request to video
### url="https://www.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics%2CtopicDetails&chart=mostPopular&pageToken=&regionCode=US&key="+api_token
# max value range [0,50]
## sample api - APIKEY, channelId- UCsT0YIqwnpJCM-mx7-gSA4Q
outerurl="https://www.googleapis.com/youtube/v3/search?key="+api_token+"&channelId="+channel+"&part=id&order=date&maxResults=50"
innerurl="https://www.googleapis.com/youtube/v3/videos?id=Ks-_Mh1QhMc,c0KYU2j0TM4,eIho2S0ZahI&part=snippet,contentDetails,statistics,topicDetails&regionCode=US&key=APIKEY"
mylist = []
mycounts = {}
totalcount = (int(size)/50)%200
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
#                if i["contentDetails"]["caption"] == "true":        ## compute only if capions are present
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
                os.system("sh $HOME/Keyword_Recommender/scripts/extractor.sh "+i["id"])
    else:
        break
    if 'nextPageToken' not in jsonObj:
        break
    outerurl = outerurl="https://www.googleapis.com/youtube/v3/search?key="+api_token+"&channelId="+channel+"&part=id&order=date&maxResults=50&pageToken=" + \
          jsonObj["nextPageToken"] + "&regionCode=US"
    totalcount=totalcount-1
