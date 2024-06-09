import os
import json
import requests

def main(minquality = 720, islektor = True, isdubbing = True, ispl = True, isnapisy = False, isnapisy_transl = False, isdubbing_kino = False, iseng = False):
    with open('movies.json', 'r') as file:
        data = json.load(file)

    for movie in data:
        print()
        print(movie["title"])
        # print("Przebrane filmy: ")
        for element in movie["urls"]:
            if((element["version"] == 'Lektor' and islektor) 
            or (element["version"] == 'Dubbing' and isdubbing) 
            or (element["version"] == 'PL' and ispl)
            or (element["version"] == 'Napisy' and isnapisy)
            or (element["version"] == 'Napisy_Tansl' and isnapisy_transl)
            or (element["version"] == 'Dubbing_kino' and isdubbing_kino) 
            or (element["version"] == 'ENG' and iseng)):
                if(element["quality"] >= minquality):
                    print(element["url"])
                    url = 'http://10.0.0.100:3128/linkcollector/addLinks?links='+element["url"]+'&packageName='+ movie["title"] +'&extractPassword&downloadPassword'
                    response = requests.get(url=url)
                    # if(response.status_code == 200):
                    #     print("API sent successfully ")
        input()
        url = 'http://10.0.0.100:3128/linkgrabberv2/clearList'
        response = requests.get(url)
        if(response.status_code == 200):
            print("Successfully cleared list")
        url = 'http://10.0.0.100:3128/linkgrabberv2/abort'
        response = requests.get(url)
        if(response.status_code == 200):
            print("Successfully aborted jobs")
                    