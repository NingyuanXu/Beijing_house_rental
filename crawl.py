from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import csv
import time
import lxml


url = "https://bj.58.com/pinpaigongyu/pn/{page}/?minprice=2000_4000"

page = 0

# open csv file with write mode
csv_file = open("rent.csv", "w", -1, "UTF-8")
csv_writer = csv.writer(csv_file, delimiter=',')

while True:

    page += 1
    print("fetch: ", url.format(page=page))
    time.sleep(5)
    # 爬取信息
    response = requests.get(url.format(page=page))
    # 处理html
    html = BeautifulSoup(response.text,features="lxml")
    house_list = html.select(".list > li")

    if not house_list:
        break

    for house in house_list:
        house_title = house.select("h2")[0].string
        house_url = house.select("a")[0]["href"]
        house_info_list = house_title.split()

        if "公寓" in house_info_list[1] or "青年社区" in house_info_list[1]:
            house_location = house_info_list
        else:
            house_location = house_info_list[1]

        house_money = house.select(".money")[0].select("b")[0].string
        csv_writer.writerow([house_title, house_location, house_money, house_url])

csv_file.close()