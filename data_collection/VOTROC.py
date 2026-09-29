import requests as req
import bs4
import json

url = "https://zh.wikipedia.org/wiki/%E4%B8%AD%E8%8F%AF%E6%B0%91%E5%9C%8B%E6%9D%91%E9%87%8C%E5%88%97%E8%A1%A8"
res = req.get(url)
soup = bs4.BeautifulSoup(res.text, "html.parser")

# find all table class="wikitable" in html
table = soup.find_all("table", class_="wikitable")
Cities = [
    "臺北市",
    "新北市",
    "基隆市",
    "桃園市",
    "新竹市",
    "新竹縣",
    "宜蘭縣",
    "苗栗縣",
    "臺中市",
    "彰化縣",
    "南投縣",
    "雲林縣",
    "嘉義市",
    "嘉義縣",
    "臺南市",
    "高雄市",
    "屏東縣",
    "澎湖縣",
    "花蓮縣",
    "臺東縣",
    "金門縣",
    "連江縣",
]

# Prepare data structure to store the information
data = {}
for city in Cities:
    data[city] = []
    tr = table[Cities.index(city)].find_all("tr")
    # find all td in tr # 區域欄位
    for i in range(1, len(tr) - 1):
        td = tr[i].find_all("td")  # 控制
        sector = td[0].text
        # find all a in td # 村里欄位
        a = td[1].find_all("a")
        # find all text in a # 村里名稱
        villages = [a[i].text for i in range(0, len(a))]
        data[city].append({sector: villages})

# Write data to a json file
with open("result.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)
