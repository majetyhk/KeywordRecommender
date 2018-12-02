import requests
import json
import sys
import os
os.system("mkdir -p output/")
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

url ="https://www.googleapis.com/youtube/v3/videos?part=snippet%2Cstatistics&chart=mostPopular&pageToken=&regionCode=US&key="+api_token

mylist = []
mycounts = {}
totalcount = (int(size)/5)%200
data ={}
while(totalcount>0):
    r = requests.get(url,headers={"Content-Type": "application/json"})
    jsonObj  = r.json()
    if (r.status_code==200  or r.status_code == 304) and (len(jsonObj)!=0):
        for i in jsonObj["items"]:
            data['id'] = i["id"]
            data['title'] = i["snippet"]["title"]
            if 'tags' in i["snippet"]:
                data['tags'] = i["snippet"]["tags"]
            data['categoryId'] = i["snippet"]["categoryId"]
            data['statistics'] = i["statistics"]
            with open('./output/'+i["id"]+'.json', 'w') as outfile:
                json.dump(data, outfile)
    else:
        break
    url = "https://www.googleapis.com/youtube/v3/videos?part=snippet%2Cstatistics&chart=mostPopular&pageToken=" + \
          jsonObj["nextPageToken"] + "&regionCode=US&key=" + api_token
    totalcount=totalcount-1