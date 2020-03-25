import json
import requests
import time





thisYearAndMonth = int(time.strftime('%Y%m', time.localtime(time.time())))

URL = "http://open.neis.go.kr/hub/mealServiceDietInfo?KEY=c371677ff44c4a8098f584586348e985&ATPT_OFCDC_SC_CODE=K10&SD_SCHUL_CODE=7800076&MLSV_FROM_YMD="+str(thisYearAndMonth)+"&MLSV_TO_YMD"+str(thisYearAndMonth+2)+"&Type=json"


response = requests.get(URL) 

data = json.loads(response.text)

print(data)