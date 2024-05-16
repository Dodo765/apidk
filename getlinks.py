import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import re
import base64
import unicodedata

def main(movie_url, minSeason = 0, maxSeason = 99999, minEpisode = 0, maxEpisode = 9999):

    # Adres strony logowania
    login_url = "https://filman.cc/logowanie"


    movie_urls = []

    # Dane logowania
    username = "ditroi"
    password = "Pa$$w0rd"

    def to_ascii(s):
        return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')


    driver = webdriver.Chrome()

    driver.get(login_url)

    driver.implicitly_wait(2.5)

    logininput = driver.find_element(by=By.ID, value="input-login")
    pwdinput = driver.find_element(by=By.ID, value="input-password")
    submitbtn = driver.find_element(by=By.XPATH, value="/html/body/div[6]/div/form/div/button")

    logininput.send_keys(username)
    pwdinput.send_keys(password)
    submitbtn.click()

    driver.implicitly_wait(0.5)

    if(movie_url.find("movies")>=0 or movie_url.count("/")>6):
        print("Founded movie")
        movie_urls.append(movie_url)
        
    elif(movie_url.find("serial-online")>=0):
        print("Founded serial")
        print("Looking from "+ str(minSeason)+" season to "+str(maxSeason) + " season")
        print("Looking from "+ str(minEpisode)+" episode to "+str(maxEpisode) + " episode")
        print("Getting links of:")
        
        driver.get(movie_url)
        driver.implicitly_wait(8.5)
        
        allepisodes = driver.find_element(By.CSS_SELECTOR, '#episode-list')
        seasons = allepisodes.find_elements(By.CSS_SELECTOR, '#episode-list>li')
        seasons.reverse()
        links = []
        
        for season in seasons:
            title = season.find_element(By.CSS_SELECTOR, 'span').text
            title = int(title[6:])
            if(title >= minSeason and title <= maxSeason):
                episodes = season.find_elements(By.CSS_SELECTOR, 'a')
                episodes.reverse()
                for episode in episodes:
                    nr = int(episode.text[5:7])
                    if(nr>=minEpisode and nr <= maxEpisode):
                        url = episode.get_attribute('href')
                        links.append(url) 
        movie_urls = links
    else:
        print("Missing links for this episode/movie")

    data = []
    
    #per movie code
    for movie in movie_urls:
        driver.get(str(movie))

        title = driver.title[:-46]
        title = to_ascii(title)

        print(title)

        linkstable = driver.find_element(by=By.ID, value='links')

        linkstr = linkstable.find_elements(by=By.CLASS_NAME, value='visible-1')

        moviedata={"title": title, "urls":[]}

        for tr in linkstr:
            # print("")
            
            classes = tr.get_attribute('class')        
            match = re.search(r'\bversion-\w+', classes)
            if match:
                version = match.group(0)
                version = version[8:]
            # print(version)

            
            try:
                td = tr.find_element(by=By.CSS_SELECTOR, value=".link-to-video")
                a = td.find_element(by=By.CSS_SELECTOR, value='a')
                quality = tr.find_element(by=By.CSS_SELECTOR, value='td:nth-child(3)')
                quality = quality.text[:-1]
                quality = int(quality)
                # print(quality)
                
            except:
                print("nie ma filmów")
            else:
                encoded = a.get_attribute('data-iframe')
                decoded = base64.b64decode(encoded)
                url = json.loads(decoded)
                src_value = url["src"]
                img = a.find_element(By.CSS_SELECTOR, 'img')
                img = img.get_attribute('alt')
                moviedata["urls"].append({"url":src_value, "quality":quality, "version":version, "provider": img})
        
        data.append(moviedata)
        
    with open('movies.json', 'w') as f:
        json.dump(data, f)

    print("******************************************")
    driver.quit()
