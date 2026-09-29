import mysql.connector

# MySQL連接參數
from config import MYSQL_CONFIG as mysql_config


def addRecord(data):
    SQL_str=""
    print(data)
    Age = data.get('Age') #0-5 `18 歲以下`, `18-24 歲`, `25-34 歲`, `35-44 歲`, `45-54 歲`, `55 歲以上`
    if Age == "0":
        SQL_str +="`18 歲以下`,"
    elif Age == "1":
        SQL_str +="`18-24 歲`,"
    elif Age == "2":
        SQL_str +="`25-34 歲`,"
    elif Age == "3":
        SQL_str +="`35-44 歲`,"
    elif Age == "4":
        SQL_str +="`45-54 歲`,"
    elif Age == "5":
        SQL_str +="`55 歲以上`,"
    CityTravelDays = data.get('CityTravelDays') #0-1 `大眾運輸2`, `自駕2`,
    if CityTravelDays == "0":
        SQL_str +="`大眾運輸2`,"
    elif CityTravelDays == "1":
        SQL_str +="`自駕2`,"
    Gender = data.get('Gender') #0-3 `男`, `女`, `其他`, `其他`
    if Gender == "0":
        SQL_str +="`男`,"
    elif Gender == "1":
        SQL_str +="`女`,"
    else:
        SQL_str +="`其他`,"
    Job = data.get('Job') #0-6 `學生`, `家管`, `工商業人員`, `自由業`, `軍/警/公/教/人員`, `醫護人員` `其他`,
    if Job == "0":
        SQL_str +="`學生`,"
    elif Job == "1":
        SQL_str +="`家管`,"
    elif Job == "2":
        SQL_str +="`工商業人員`,"
    elif Job == "3":
        SQL_str +="`自由業`,"
    elif Job == "4":
        SQL_str +="`軍/警/公/教/人員`,"
    elif Job == "5":
        SQL_str +="`醫護人員`,"
    else:
        SQL_str +="`其他`,"
    MtTravelType = data.get('MtTravelType')#0-1 `大眾運輸1`, `自駕1`,
    if MtTravelType == "0":
        SQL_str +="`大眾運輸1`,"
    elif MtTravelType == "1":
        SQL_str +="`自駕1`,"
    PurchasedItem = data.get('PurchasedItem')#0-3 `不太購買商品`, `奢侈品等高檔商品`, `當地土產、特產`, `當地手工藝品、文化用品等特色商品`
    if PurchasedItem == "0":
        SQL_str +="`不太購買商品`,"
    elif PurchasedItem == "1":
        SQL_str +="`奢侈品等高檔商品`,"
    elif PurchasedItem == "2":
        SQL_str +="`當地土產、特產`,"
    else:
        SQL_str +="`當地手工藝品、文化用品等特色商品`,"
    TravelDays = data.get('TravelDays')#0-4 `days`
    SQL_str +="`days`,"
    TravelDaysBudget1 = data.get('TravelDaysBudget1')#0-3 `budget1Day`
    SQL_str +="`budget1Day`,"
    TravelDaysBudget2 = data.get('TravelDaysBudget2')#0-3 `budget2Day`
    SQL_str +="`budget2Day`,"
    TravelDaysBudget3 = data.get('TravelDaysBudget3')#0-3 `budget3-4Day`
    SQL_str +="`budget3-4Day`,"
    TravelDaysBudget5 = data.get('TravelDaysBudget5')#0-3 `budget5-6Day`
    SQL_str +="`budget5-6Day`,"
    TravelDaysBudget7 = data.get('TravelDaysBudget7')#0-3 `budget7Day`
    SQL_str +="`budget7Day`,"
    TravelInfo = data.get('TravelInfo')#0-4 `旅遊公司官方網站或實體店面`, `旅遊書籍或雜誌`, `旅遊相關網站或APP`, `朋友親戚或同事推薦`, `網路搜尋引擎`,
    if TravelInfo == "0":
        SQL_str +="`旅遊公司官方網站或實體店面`,"
    elif TravelInfo == "1":
        SQL_str +="`旅遊書籍或雜誌`,"
    elif TravelInfo == "2":
        SQL_str +="`旅遊相關網站或APP`,"
    elif TravelInfo == "3":
        SQL_str +="`朋友親戚或同事推薦`,"
    else:
        SQL_str +="`網路搜尋引擎`,"
    TravelMedia = data.get('TravelMedia')#0-3 `Google Maps`, `Vlog／部落格`,  `旅遊網站／APP`, `其他方式`
    if TravelMedia == "0":
        SQL_str +="`Google Maps`,"
    elif TravelMedia == "1":
        SQL_str +="`Vlog／部落格`,"
    elif TravelMedia == "2":
        SQL_str +="`旅遊網站／APP`,"
    else:
        SQL_str +="`其他方式`,"
    TravelNeeds = data.get('TravelNeeds')#0-5 `不用看到討厭的人`, `增長見聞、學習新技能`, `放鬆身心、紓解壓力`, `獨立探險、尋找新鮮感`, `與親友共遊、增進感情`, `體驗當地文化、風俗習慣`,
    if TravelNeeds == "0":
        SQL_str +="`不用看到討厭的人`,"
    elif TravelNeeds == "1":
        SQL_str +="`增長見聞、學習新技能`,"
    elif TravelNeeds == "2":
        SQL_str +="`放鬆身心、紓解壓力`,"
    elif TravelNeeds == "3":
        SQL_str +="`獨立探險、尋找新鮮感`,"
    elif TravelNeeds == "4":
        SQL_str +="`與親友共遊、增進感情`,"
    else:
        SQL_str +="`體驗當地文化、風俗習慣`,"
    TravelPeople = data.get('TravelPeople')#0-3 `1 個人`, `2 個人`, `3~5 人`, `6 人以上`
    if TravelPeople == "0":
        SQL_str +="`1 個人`,"
    elif TravelPeople == "1":
        SQL_str +="`2 個人`,"
    elif TravelPeople == "2":
        SQL_str +="`3~5 人`,"
    else:
        SQL_str +="`6 人以上`,"
    TravelSchedule = data.get('TravelSchedule')#0-3 `一周前或更短時間`, `一周 ~ 一個月前`, `一個月 ~ 三個月前`, `三個月 ~ 六個月前`
    if TravelSchedule == "0":
        SQL_str +="`一周前或更短時間`,"
    elif TravelSchedule == "1":
        SQL_str +="`一周 ~ 一個月前`,"
    elif TravelSchedule == "2":
        SQL_str +="`一個月 ~ 三個月前`,"
    else:
        SQL_str +="`三個月 ~ 六個月前`,"
    TravelType = data.get('TravelType')#0-3  `自助旅行`, `跟團旅行`, `都喜歡`, `其他旅遊方式`,
    if TravelType == "0":
        SQL_str +="`自助旅行`,"
    elif TravelType == "1":
        SQL_str +="`跟團旅行`,"
    elif TravelType == "2":
        SQL_str +="`都喜歡`,"
    else:
        SQL_str +="`其他旅遊方式`,"
    userID = data.get('userID')
    if not userID:
        return False, 'userID is required'
    # 每位使用者只填一次（2023 版會重複寫入多列，且 finally 裡的 return 讓失敗也回報成功）
    if ifRecord(userID):
        return False, 'isRecord.'
    conn = None
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        sql=f"INSERT INTO `userPreferences` ({SQL_str} `userID`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val=(1, 1, 1, 1, 1, 1, TravelDays, TravelDaysBudget1, TravelDaysBudget2, TravelDaysBudget3, TravelDaysBudget5, TravelDaysBudget7, 1, 1, 1, 1, 1, 1, userID)
        cursor.execute(sql, val)
        conn.commit()
        return True, 'addRecord successful'
    except Exception as e:
        print(e)
        return False, str(e)
    finally:
        if conn is not None:
            conn.close()


def ifRecord(userid):
    sql = "SELECT * FROM `userPreferences` WHERE `userID` = %s"
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(buffered=True)
        cursor.execute(sql, (userid,))
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
    finally:
        conn.close()