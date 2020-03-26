# -*- encoding: utf-8 -*-


import json
import time
import requests
import re
import bs4, urllib.request


p = re.compile("[^0-9]")

apiKeyFIle = open("C:\\Users\\yju08\\OneDrive\\동기화폴더\\서버용폴더\\YJUBOT\\secretData\\apikey.txt",encoding="utf-8")
apiKey = apiKeyFIle.read()
apiKeyFIle.close()



def UpdateDatabase():
    thisYearAndMonth = int(time.strftime('%Y%m', time.localtime(time.time())))

    URL = "http://open.neis.go.kr/hub/mealServiceDietInfo?KEY="+ apiKey +"&ATPT_OFCDC_SC_CODE=K10&SD_SCHUL_CODE=7800076&MLSV_FROM_YMD="+str(thisYearAndMonth)+"&MLSV_TO_YMD"+str(thisYearAndMonth+2)+"&Type=json"
    response = requests.get(URL) 
    print(URL)
    data = json.loads(response.text)

    for i in range(len(data["mealServiceDietInfo"][1]["row"])):
        data["mealServiceDietInfo"][1]["row"][i]["DDISH_NM"] = "".join(p.findall(data["mealServiceDietInfo"][1]["row"][i]["DDISH_NM"].replace("<br/>","\n").replace(".","")))
    
    f = open("C:\\Users\\yju08\\OneDrive\\동기화폴더\\서버용폴더\\YJUBOT\\newdatabase.json","w",encoding="utf-8")
    f.write(str(data).replace("'",'"'))
    f.close()



def UpdateMusicList():


    URL = "https://www.youtube.com/playlist?list=PL5YUhynrI5ewlhZmGCEAy4_KQnMfxUNOS"
    html = urllib.request.urlopen(URL)
    bsObj = bs4.BeautifulSoup(html,"html.parser")

    songNameHTML = bsObj.find_all("a",{"class":"pl-video-title-link yt-uix-tile-link yt-uix-sessionlink spf-link"})
    singerNameHTML = bsObj.find_all("a",{"class":"yt-uix-sessionlink spf-link"})
    UrlHTML = bsObj.find_all("a",{"class":"pl-video-title-link yt-uix-tile-link yt-uix-sessionlink spf-link"})

    singerNameHTML.remove(singerNameHTML[0])

    imageHTML = bsObj.find_all("img",{"alt":""})

    for i in imageHTML[:]:
        if i.get("data-thumb") == None or i.get("data-thumb").startswith("http") == False:
            imageHTML.remove(i)


    music = ""

    for i in range(0,len(songNameHTML)):
        music+=songNameHTML[i].text.replace("\n","")+"$"
        music+=singerNameHTML[i].text+"$"
        music+=imageHTML[i].get("data-thumb")+"$"
        music+="https://www.youtube.com/"+UrlHTML[i].get("href")+"|"
        



    f = open("C:\\Users\\yju08\\OneDrive\\동기화폴더\\서버용폴더\\YJUBOT\\musiclist.txt","w",encoding="utf-8")
    f.write(music)
    f.close()

    

if __name__ == "__main__":
    while True:
        updatetime=time.strftime('%H', time.localtime(time.time()))
        if updatetime=="15":
            UpdateDatabase()
            UpdateMusicList()
            print("데이터가 업데이트 되었습니다.[{}]".format(time.strftime('%c', time.localtime(time.time()))))
            time.sleep(86400)


