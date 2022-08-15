import json
import urllib.request
import socket
import time
import datetime
import DataFetcher


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

companyList = []
newCompanyList = []
companyData = {}
urlApi = "https://nepsealpha.com/trading/0/history?symbol=ADBL&resolution=1D&from=1575089980&to=1610082051" \
         "&currencyCode=NRS"
dailyData = "https://newweb.nepalstock.com.np/api/nots/nepse-data/today-price?&size=500&businessDate=2021-01-10"
count = 1


def update_companies():
    global companyList
    print("\nUpdating Companies List... \n")

    with open('companies.json', 'r+') as outfile:
        companyList = json.loads(outfile.read())["content"]
    print("\nUpdating Companies List Done \n....\n")


def update_json_file():
    global hdr
    today = datetime.datetime(datetime.datetime.utcnow().year,
                              datetime.datetime.utcnow().month,
                              datetime.datetime.utcnow().day,0,0,0).replace(tzinfo= datetime.timezone.utc).timestamp()
    print("today 00:00 gmt epoch "+str(today))
    with open('companies.json', 'r+') as outfile:
        if(json.loads(outfile.read())["updatedAt"]==datetime.datetime.utcnow().strftime("%Y-%m-%d")):
            print("Already updated for today. "+ datetime.datetime.utcnow().strftime("%Y-%m-%d"))
            return
    try:
        # dailyDataURL = "https://newweb.nepalstock.com.np/api/nots/nepse-data/today-price?&size=500&businessDate=" + datetime.datetime.today().strftime(
        #     '%Y-%m-%d')
        # print("Sending http req for daily data \n" + dailyDataURL)
        #
        # request = urllib.request.Request(urlApi, None, hdr)  # The assembled request
        # with urllib.request.urlopen(request) as url:
        #   dailyjsonData = json.loads(url.read().decode())
        dailyjsonData = DataFetcher.getLatestDatafromShareSansar()
        print("got for daily data  ")
    except:
        print("Error occured sending request to nepse site")
        return

    # with open('scratch.json', 'r+') as outfile:
    #     print("Reading daily Data")
    #     dailyjsonData = json.loads(outfile.read())
    #     print("Reading daily done")

    print("today's date - ")
    print(str(datetime.datetime.utcnow().strftime("%Y-%m-%d"))) 
    print("business's date - ")
    print(str(dailyjsonData["content"][0]["businessDate"]))
    if(str(time.strftime('%Y-%m-%d', time.localtime(dailyjsonData["content"][0]["businessDate"]))) == str(datetime.datetime.utcnow().strftime("%Y-%m-%d"))):
        print("\n\nToday was a trade day!\t\tUpdating allData..\n\n")

        with open('alldata.json', 'r+') as outfile:
            print("Reading all Data")
            allData = json.loads(outfile.read())
            print("Reading all Data done")

            for compDaily in dailyjsonData["content"]:
                try:
                    if compDaily["symbol"] in allData:
                        print("updating " + compDaily["symbol"])
                        print(str(allData[compDaily["symbol"]]["data"]["t"][0]))
                        allData[compDaily["symbol"]]["data"]["t"].append(int(today))
                        allData[compDaily["symbol"]]["data"]["c"].append(float(compDaily["closePrice"]))
                        allData[compDaily["symbol"]]["data"]["o"].append(float(compDaily["openPrice"]))
                        allData[compDaily["symbol"]]["data"]["h"].append(float(compDaily["highPrice"]))
                        allData[compDaily["symbol"]]["data"]["l"].append(float(compDaily["lowPrice"]))
                        allData[compDaily["symbol"]]["data"]["v"].append(int(float(compDaily["totalTradedValue"])))
                        allData[compDaily["symbol"]]["data"]["s"] = "ok"
                    else:
                        print("Error, company not found in all-data ---------------------------- > "+compDaily["symbol"])
                        allData[compDaily["symbol"]] = {}
                        allData[compDaily["symbol"]]["data"] = {}
                        allData[compDaily["symbol"]]["data"]["t"] = []
                        allData[compDaily["symbol"]]["data"]["t"].append(int(today))
                        allData[compDaily["symbol"]]["data"]["c"] = []
                        allData[compDaily["symbol"]]["data"]["c"].append(float(compDaily["closePrice"]))
                        allData[compDaily["symbol"]]["data"]["o"] = []
                        allData[compDaily["symbol"]]["data"]["o"].append(float(compDaily["openPrice"]))
                        allData[compDaily["symbol"]]["data"]["h"]= []
                        allData[compDaily["symbol"]]["data"]["h"].append(float(compDaily["highPrice"]))
                        allData[compDaily["symbol"]]["data"]["l"] = []
                        allData[compDaily["symbol"]]["data"]["l"].append(float(compDaily["lowPrice"]))
                        allData[compDaily["symbol"]]["data"]["v"] = []
                        allData[compDaily["symbol"]]["data"]["v"].append(int(float(compDaily["totalTradedValue"])))
                        allData[compDaily["symbol"]]["data"]["s"]= "ok"
                        print("updating " + compDaily["symbol"])
                        print(str(allData[compDaily["symbol"]]["data"]["t"][0]))
                        newCompanyList.append(compDaily["symbol"])
                except:
                    print("error occured for "+compDaily["symbol"])
                    continue

        print("Writing all Data...")
        with open('alldata.json', 'w+') as outfile:
            json.dump(allData, outfile)

        companyList.extend(newCompanyList)
        with open('companies.json', 'w+') as outfile:
            companyUpdate = {"updatedAt": datetime.datetime.utcnow().strftime("%Y-%m-%d"), "content": companyList}
            json.dump(companyUpdate, outfile, indent=4)
    else:
        print("Today was no-trade day")


if __name__ == '__main__':
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print("IP: "+ip_address+"\nHostname: "+hostname)
    print(datetime.datetime.utcnow().strftime("%Y-%m-%d"))

    update_companies()
    update_json_file()
