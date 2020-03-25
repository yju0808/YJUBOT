# -*- encoding: utf-8 -*-
import json
import time
import requests
import re


p = re.compile("[^0-9]")

apiKeyFIle = open("C:\\Users\\yju08\\OneDrive\\동기화폴더\\서버용폴더\\YJU bot\\secretData\\apikey.txt",encoding="utf-8")
apiKey = apiKeyFIle.read()
apiKeyFIle.close()



def updatedatabase():
    thisYearAndMonth = int(time.strftime('%Y%m', time.localtime(time.time())))

    URL = "http://open.neis.go.kr/hub/mealServiceDietInfo?KEY="+ apiKey +"&ATPT_OFCDC_SC_CODE=K10&SD_SCHUL_CODE=7800076&MLSV_FROM_YMD="+str(thisYearAndMonth)+"&MLSV_TO_YMD"+str(thisYearAndMonth+2)+"&Type=json"
    response = requests.get(URL) 
    print(URL)
    data = json.loads(response.text)

    for i in range(len(data["mealServiceDietInfo"][1]["row"])):
        data["mealServiceDietInfo"][1]["row"][i]["DDISH_NM"] = "".join(p.findall(data["mealServiceDietInfo"][1]["row"][i]["DDISH_NM"].replace("<br/>","\n").replace(".","")))
    
    f = open("C:\\Users\\yju08\\OneDrive\\동기화폴더\\서버용폴더\\YJU bot\\newdatabase.json","w",encoding="utf-8")
    f.write(str(data).replace("'",'"'))
    f.close()

    return 0
        

    

if __name__ == "__main__":
    while True:
        updatetime=time.strftime('%H', time.localtime(time.time()))
        if updatetime=="15":
            updatedatabase()
            print("데이터가 업데이트 되었습니다.[{}]".format(time.strftime('%c', time.localtime(time.time()))))
            time.sleep(86400)

