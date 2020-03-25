from flask import Flask, request, jsonify
import json
import time
import random


app = Flask(__name__)


blockIdsfile = open("C:\\Users\\yju08\\OneDrive\\동기화폴더\\서버용폴더\\YJU bot\\secretData\\blockIds.txt",encoding="UTF-8")
blockIds = json.loads(blockIdsfile.read())
blockIdsfile.close()


def Meal(inputYear,inputMonth,inputDay,discrimination):
    year = inputYear
    month = inputMonth
    day = inputDay

    mealDataFile=open("C:\\Users\\yju08\\OneDrive\\동기화폴더\\서버용폴더\\YJU bot\\newdatabase.json",encoding="utf-8")
    mealData = json.loads(mealDataFile.read())["mealServiceDietInfo"][1]["row"]
    mealDataFile.close()


    breakfast = "해당하는 급식이 없습니다"
    lunch = "해당하는 급식이 없습니다"
    dinner = "해당하는 급식이 없습니다"


    for i in mealData:
        if i["MLSV_YMD"]=="{}{}{}".format(year,month,day) and i["MMEAL_SC_NM"]=="조식":
            breakfast = i["DDISH_NM"]

        elif i["MLSV_YMD"]=="{}{}{}".format(year,month,day) and i["MMEAL_SC_NM"]=="중식":
            lunch = i["DDISH_NM"]

        elif i["MLSV_YMD"]=="{}{}{}".format(year,month,day) and i["MMEAL_SC_NM"]=="석식":
            dinner = i["DDISH_NM"]
    
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "{}월 {}일 [조식]".format(month,day)+"\n"+breakfast+"\n\n"+ "{}월 {}일 [중식]".format(month,day)+"\n"+lunch+"\n\n"+"{}월 {}일 [석식]".format(month,day)+"\n"+dinner
                    }
                }
            ],
            "quickReplies": [
                {
                    "label":"홈으로",
                    "action":"block",
                    "blockId" : blockIds["Home"],

                },
                {
                    "label": "날짜선택",
                    "action":"block",
                    "blockId" : blockIds["SelectDate"],
                }
            ]
        }
    }

    if discrimination=="TodayMeal":
        res["template"]["quickReplies"].append({"label":"내일급식은?", "action":"block", "blockId" : blockIds["TomorrowMeal"],})
    elif discrimination=="TomorrowMeal":
        res["template"]["quickReplies"].append({"label":"오늘급식은?", "action":"block", "blockId" : blockIds["TodayMeal"],})
    elif discrimination=="SelectDate":
        res["template"]["quickReplies"].append({"label":"오늘급식은?", "action":"block", "blockId" : blockIds["TodayMeal"],})
        res["template"]["quickReplies"].append({"label":"내일급식은?", "action":"block", "blockId" : blockIds["TomorrowMeal"],})


    return res












@app.route('/TodayMeal', methods=['POST'])
def TodayMeal():

    inputYear = time.strftime('%Y', time.localtime(time.time()))
    inputMonth = time.strftime('%m', time.localtime(time.time()))
    inputDay = time.strftime('%d', time.localtime(time.time()))
    
    return jsonify(Meal(inputYear,inputMonth,inputDay,"TodayMeal"))







@app.route('/TomorrowMeal', methods=['POST'])
def TomorrowMeal():

    inputYear = time.strftime('%Y', time.localtime(time.time()))
    inputMonth = time.strftime('%m', time.localtime(time.time()))
    inputDay = time.strftime('%d', time.localtime(time.time()))

    #날짜 처리
    if int(inputMonth) in [4,6,9,11] and int(inputDay) == 30:
        if inputMonth == 12:
            inputYear = str(int(inputYear)+1)
            inputMonth = "01"
            inputDay= "01"
        else:
            inputMonth = str(int(inputYear)+1)
            if len(inputMonth)==1:
                inputMonth = "0"+inputMonth
            inputDay="01"
    else:
        inputDay = str(int(inputDay)+1)
        if len(inputDay)==1:
                inputDay = "0"+inputDay


    return jsonify(Meal(inputYear,inputMonth,inputDay,"TomorrowMeal"))











@app.route('/SelectDate', methods=['POST'])
def SelectDate():

    req = request.get_json()
    date = json.loads(req["action"]["detailParams"]["date"]["value"])["value"].split("-")

    inputYear = date[0]
    inputMonth = date[1]
    inputDay = date[2]

    return jsonify(Meal(inputYear,inputMonth,inputDay,"SelectDate"))











@app.route('/music', methods=['POST'])
def music():
    musicListFile = open("C:\\Users\\yju08\\OneDrive\\동기화폴더\\서버용폴더\\YJU bot\\musiclist.txt",encoding="utf-8")
    musicList = musicListFile.read().split("\n\n")
    musicListFile.close()

    musicAndURL = random.choice(musicList).split("|")
    music = musicAndURL[0]
    URL = musicAndURL[1]

    res = {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "carousel": {
                "type": "basicCard",
                "items": [
                {
                    "title": music,
                    "description": URL,
                    "thumbnail": {
                    "imageUrl": "https://ifh.cc/g/8NMLi.png"
                    }
                }

            ]
        }
    }
    ],
    "quickReplies":[
    {
      "label":"홈으로",
      "action":"block",
      "blockId" : blockIds["Home"],

    },
    {
      "label":"음악추천 더해줘",
      "action":"block",
      "blockId" : blockIds["MusicRecommendation"],

    },
    {
      "label":"음악 더보기",
      "action":"block",
      "blockId" : blockIds["MoreMusic"],

    }
    ]
    }
    }

    return jsonify(res)












# 메인 함수
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
