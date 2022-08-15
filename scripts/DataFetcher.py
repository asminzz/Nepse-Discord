# importing the libraries
import json
import time, datetime

from bs4 import BeautifulSoup
import urllib.request, urllib.parse
import urllib3
import html, calendar


class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"


opener = AppURLopener()
hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'origin': 'https://newweb.nepalstock.com.np',
        'referer': 'https://newweb.nepalstock.com.np/today-price',
        'Connection': 'keep-alive'
}

def getLatestDatafromShareSansar():
    dailyDataURL = "https://www.sharesansar.com/today-share-price"
    global opener, hdr
    print("Pulling from sharesansar")

    request = urllib.request.Request(dailyDataURL, None, hdr)  # The assembled request
    with urllib.request.urlopen(request) as url:
        dailyData = (str(url.read())).rstrip("\n")
        with open('sharesansarDailyData.txt', 'w+') as outfile:
            outfile.write(dailyData)


    with open('sharesansarDailyData.txt', 'r+') as outfile:
        dailyData = (outfile.read())

        # Parse the html content
        soup = BeautifulSoup(str(dailyData), "html.parser")
        soup.prettify()
        print(soup.title.text)

        gdp_table = soup.find("table", attrs={"class": "dataTable"})
        gdp_table_data = gdp_table.tbody.find_all("tr")  # contains 2 rows

        print(gdp_table_data[0].find_all("td")[1].get_text().replace("\\n", "").strip())
        n = gdp_table_data[0].find_all("td")[1].get_text().replace("\n", "")
        print(n)

        dailyJson = {}
        dailyJson["content"]= []

        dt = str(soup.find("span", attrs={"class": "text-org"}).get_text().replace('\\n', ' ').strip())+" "
        ti = "20:45:00"
        dt_ti = dt + ti
        pattern = '%Y-%m-%d %H:%M:%S'
        businessDate = (int(calendar.timegm(time.strptime(dt_ti, pattern))))
        print(businessDate)
        for td in gdp_table_data:
            dailyJson["content"].append(
                {
                    "businessDate": businessDate,
                    "symbol": str(td.find_all("td")[1].get_text().replace('\\n', ' ').replace(',', '').strip()),
                    "openPrice": str(td.find_all("td")[3].get_text().replace('\\n', ' ').replace(',', '').strip()),
                    "highPrice": str(td.find_all("td")[4].get_text().replace('\\n', ' ').replace(',', '').strip()),
                    "lowPrice": str(td.find_all("td")[5].get_text().replace('\\n', ' ').replace(',', '').strip()),
                    "closePrice": str(td.find_all("td")[6].get_text().replace('\\n', ' ').replace(',', '').strip()),
                    "totalTradedValue": str(td.find_all("td")[8].get_text().replace('\\n', ' ').replace(',', '').replace(',', '').strip())
                }
            )

        print(dailyJson)
        return dailyJson


def getLatestDatafromNEPSE():
    hdr1 = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-length': '10',
        'content-type': 'application/json',
        'origin': 'https://newweb.nepalstock.com.np',
        'referer': 'https://newweb.nepalstock.com.np/today-price',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'
    }
    global opener, hdr

    # dailyDataURL = "https://newweb.nepalstock.com.np/api/nots/nepse-data/today-price?&size=500&businessDate=" + datetime.datetime.today().strftime('%Y-%m-%d')
    dailyDataURL = "https://newweb.nepalstock.com.np/api/nots/nepse-data/today-price?&size=20&businessDate=2021-06-17"
    siteURL = "https://newweb.nepalstock.com.np/api/nots/nepse-data/market-open"

    print("Sending http req for daily data \n" + siteURL)

    dummyData = [147, 117, 239, 143, 157, 312, 161, 612, 512, 804, 411, 527, 170, 511, 421, 667, 764, 621, 301, 106,
                 133, 793, 411, 511, 312, 423, 344, 346, 653, 758, 342, 222, 236, 811, 711, 611, 122, 447, 128, 199,
                 183, 135, 489, 703, 800, 745, 152, 863, 134, 211, 142, 564, 375, 793, 212, 153, 138, 153, 648, 611,
                 151, 649, 318, 143, 117, 756, 119, 141, 717, 113, 112, 146, 162, 660, 693, 261, 362, 354, 251, 641,
                 157, 178, 631, 192, 734, 445, 192, 883, 187, 122, 591, 731, 852, 384, 565, 596, 451, 772, 624, 691]
    # id = 0
    request = urllib.request.Request(siteURL, None, hdr)  # The assembled request
    with urllib.request.urlopen(request) as url:
        idJSON = json.loads(url.read().decode())['id']
        print('idjson is ' + str(idJSON))
        id = idJSON + dummyData.__getitem__(idJSON) + (2*datetime.date.today().day)
        print('val is '+str(id))

        encoded_body = json.dumps({"id": id})

        http = urllib3.PoolManager()

        r = http.request('POST', dailyDataURL,
                         headers={'Content-Type': 'application/json'},
                         body=encoded_body)
        print(r.data.decode('utf-8'))

    # request = urllib.request.Request(dailyDataURL, data=myobj, headers=hdr1)  # The assembled request
    # with urllib.request.urlopen(request) as url:
    #     dailyJSON = json.loads(url.read().decode())
    #     print('today ko data is \n'+str(dailyJSON))

    print("http req got for daily data  ")



if __name__ == '__main__':
    # getLatestDatafromNEPSE()
    getLatestDatafromShareSansar()

