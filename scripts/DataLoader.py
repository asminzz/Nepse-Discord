import json
import urllib.request
import socket
import time
import datetime


hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

companyList = []
companyData = {}
buyData = {}
sellData = {}
sorted_buy = {}
sorted_sell = {}
textFile = "../dump/adbl.json"
urlApi = "https://nepsealpha.com/trading/0/history?symbol=ADBL&resolution=1D&from=1575089980&to=1610082051" \
         "&currencyCode=NRS"
count = 1


def update_companies():
    global companyList
    global hdr
    print("\nUpdating Companies ... \n")
    with open('companies.json', 'r+') as outfile:
        companyList = json.loads(outfile.read())["content"]
        urlApi = "https://nepsealpha.com/trading/0/search?limit=500&query=&type=&exchange="
        print("Sending http req for companies \n" + urlApi)
        
        request = urllib.request.Request(urlApi, None, hdr)  # The assembled request
        with urllib.request.urlopen(request) as url:
            jsonData = json.loads(url.read().decode())
        
        print("http req got for companies ")
        for comp in jsonData:
            if(comp["symbol"] not in companyList):
                print("Company found : "+comp["symbol"])
                companyList.append(str(comp["symbol"]))
    companyList = sorted(companyList)
    with open('companies.json', 'w+') as outfile:
        companyUpdate = {"updatedAt": datetime.datetime.utcnow().strftime("%Y-%m-%d"), "content": companyList}
        json.dump(companyUpdate, outfile, indent=4)
        
        
def update_json_file():
    print(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime(1575089980)))
    with open('alldata.json', 'w+') as outfile:
        for c in companyList:
            try:
                companyData[c] ={
                    "symbol": c,
                    "data": get_company_data_json(c)
                }
            except:
                print("Error occured while fetching "+c)
                continue
        json.dump(companyData, outfile)
        
        
def get_company_data_json(companyname):
    global textFile
    # urlApi = "https://nepsealpha.com/trading/0/history?symbol="+companyname+"&resolution=1D&from=1575089980&to=1610082051&currencyCode=NRS"
    #urlApi = "https://nepsealpha.com/trading/0/history?symbol="+companyname+"&resolution=1D&from=937586861&to=1739318400&currencyCode=NRS"
    #For unadjusted chart, just set &adjust  = 0 in below's url
    urlApi = "https://merolagani.com/handlers/TechnicalChartHandler.ashx?type=get_advanced_chart&symbol="+companyname+"&resolution=1D&rangeStartDate=937586861&rangeEndDate=1739318400&from=&isAdjust=1&currencyCode=NPR"
    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'Accept': '*/*'
    }
    print("Sending http req to \n"+urlApi)
    request = urllib.request.Request(urlApi, None, hdr)  # The assembled request
    with urllib.request.urlopen(request) as url:
        jsonData = json.loads(url.read().decode())
    print("http req got for "+companyname)
    return jsonData
    
    
def read_json():
    global textFile
    global urlApi
    f = open(textFile, "r")
    jsonData = json.loads(f.read())
    return jsonData


if __name__ == '__main__':
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print("IP: "+ip_address+"\nHostname: "+hostname)
    update_companies()
    update_json_file()
