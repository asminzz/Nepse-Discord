import json
import datetime
import time
import socket
from datetime import datetime as dt
from statistics import pstdev
import SendMessage

companyList = []
updatedAt= 0.0


def analyzeBollingerBands():
    today = datetime.datetime(datetime.datetime.utcnow().year,
                              datetime.datetime.utcnow().month,
                              datetime.datetime.utcnow().day, 0, 0, 0).replace(tzinfo=datetime.timezone.utc).timestamp()
    bbData = {}
    companyName = {"CHDC", "NICLBSL", "BNT", "UNL"}
    buylist = {}
    selllist = {}

    with open('alldata.json', 'r+') as outfile:
        global updatedAt
        print("Reading all Data")
        allData = json.loads(outfile.read())
        print("Reading all Data done")
        # print(companyList)
        # for companyName in companyList:
        for companyName in companyName:
            try:
                if (updatedAt != datetime.datetime.fromtimestamp(time.mktime(time.gmtime(
                    allData[companyName]["data"]["t"][len(allData[companyName]["data"]["t"]) - 1]))).strftime("%Y-%m-%d")):

                    print(str(companyName) + " has not been traded for " + str(updatedAt)+" but at "+str(datetime.datetime.fromtimestamp(time.mktime(time.gmtime(
                    allData[companyName]["data"]["t"][len(allData[companyName]["data"]["t"]) - 1]))).strftime("%Y-%m-%d")))
                    continue

                print("Evaluating "+companyName)
                bbData = getBollingerBands(data= allData[companyName]["data"], span=10, period= 20, multiplier= 2)
                if bbData != -1:
                    stockData = allData[companyName]["data"]
                    if getConvergence(bollingerBandsData= bbData, stockData= stockData, timeSpan= 3):
                        print(str(stockData["l"][-1])+" lower than" +str(bbData["lower"][-1]))
                        buylist[companyName]= 100*((stockData["l"][-2] - stockData["l"][-1])/stockData["l"][-2])
                    if getDivergence(bollingerBandsData= bbData, stockData= stockData, timeSpan= 3):
                        print(str(stockData["h"][-1])+" upper than" +str(bbData["upper"][-1]))
                        # selllist[companyName]= (stockData["h"][-1] - bbData["upper"][-1])
                        selllist[companyName]= 100*((stockData["h"][-1] - stockData["h"][-2])/stockData["h"][-2])

            except:
                print("Error in --------------------------------> "+companyName)
                continue

    # buylist = {k: v for k, v in sorted(buylist.items(), key=lambda item: item[1], reverse= True)}
    buylist = {k: v for k, v in sorted(buylist.items(), key=lambda item: item[1])}
    selllist = {k: v for k, v in sorted(selllist.items(), key=lambda item: item[1])}

    print("Buy the following scripts : \n")
    for c in buylist:
        print(c)
    print("\n\nSell the following scripts : \n")
    for c in selllist:
        print(c)

    now = dt.now() # current date and time
    date_timenow = now.strftime("%m/%d/%Y, %H:%M:%S")
    SendMessage.send_BollingerBand_message(buylist, selllist)
    try:
        with open('BollingerOutput.txt', 'w') as outfile:
            outfile.write("Updated at ")
            outfile.write(date_timenow)
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            outfile.write("\n")
            outfile.write(f"Hostname: {hostname}")
            outfile.write(f"IP Address: {ip_address}")

            outfile.write("\nBUY WATCH (Low price below lower band):")
            json.dump(buylist, outfile, indent=4)
            outfile.write("\n\nSELL WATCH (high price above upper band):")
            json.dump(selllist, outfile, indent=4)

    except:
        print("error")
        return True

def getConvergence(bollingerBandsData, stockData, timeSpan):
    # t = timeSpan
    #
    # c = len(bollingerBandsData["stochRSID"]) - timeSpan
    # d = []
    # while (c < len(bollingerBandsData["stochRSID"])):
    #     d.append(bollingerBandsData["stochRSID"][c] - bollingerBandsData["stochRSIK"][c])
    #     c = c + 1
    #
    # # timeSeries = allData[companyName]["data"]["t"]
    # # while (c <= len(d)):
    #
    # x = d[-t: len(d)]
    # srtX = sorted(x, reverse=True)
    # if (x == srtX):
    #     # print(x)
    #     if (8 > d[len(d)-1]):
    #         # print(d[len(d) - t])
    #         # print(d[len(d) - 1])
    #         # print("Buy signal at " + str(t))#str(datetime.datetime.fromtimestamp(timeSeries[len(timeSeries) - len(d) + c - 1]).strftime('%Y-%m-%d')))
    #         print(x)
    #         return True
    #     # c = c + 1
    # return False
    t= 1
    while(t<= timeSpan):
        if (bollingerBandsData["lower"][-t] > stockData["l"][-t]):
            return True
        t= t+1
    return False


def getDivergence(bollingerBandsData, stockData, timeSpan):
    # t = timeSpan
    #
    # c = len(bollingerBandsData["stochRSID"]) - timeSpan
    # d = []
    # while (c < len(bollingerBandsData["stochRSID"])):
    #     d.append(bollingerBandsData["stochRSID"][c] - bollingerBandsData["stochRSIK"][c])
    #     c = c + 1
    #
    # # timeSeries = allData[companyName]["data"]["t"]
    # # while (c <= len(d)):
    #
    # x = d[-t: len(d)]
    # srtX = sorted(x, reverse=False)
    # if (x == srtX):
    #     # print(x)
    #     if (-8 < d[len(d)-1]):
    #         # print(d[len(d) - t])
    #         # print(d[len(d) - 1])
    #         # print("Buy signal at " + str(t))#str(datetime.datetime.fromtimestamp(timeSeries[len(timeSeries) - len(d) + c - 1]).strftime('%Y-%m-%d')))
    #         print(x)
    #         return True
    #     # c = c + 1
    # return False
    t = 1
    while (t <= timeSpan):
        if (bollingerBandsData["upper"][-t] < stockData["h"][-t]):
            return True
        t= t+1
    return False


# Calculates the EMA (wilders' 1/n) of an array
def get_ema_wilder(data, period):
    if len(data) < period:
        print("No enough data to calculate wilder's ema")
        return -1
    ema= []
    ema.append(sum(data[0:period])/period)
    c = period
    while c < len(data):
        # print("EMA for "+str(c)+"th day is ")
        ema.append(((ema[len(ema)-1]*(period-1))+data[c])/period)
        # print(ema[len(ema)-1])
        c=c+1
    return ema


def get_sma(data, period):
    if len(data) < period:
        print("No enough data to calculate sma")
        return -1

    sma= []
    c = period
    while c <= len(data):
        sma.append(sum(data[c-period:c])/period)
        c=c+1
    return sma


def get_typical_price(data):
    tp= []
    c = 0
    while c < len(data["c"]):
        tp.append( (data["c"][c]+data["h"][c]+data["l"][c]) / 3 )
        c=c+1
    return tp


def getBollingerBands(data, span= 10, period= 20, multiplier= 2):
    sma= get_sma(data["c"], period)
    bandMid= sma
    # print(sma)
    bandUpper= []
    bandLower= []

    if len(data["c"]) < period:
        print("data not enough")
        return -1

    i= period
    while i<= (len(data["t"])):
        sd = pstdev(data["c"][i-period:i])
        bandUpper.append(sma[i-period]+ (multiplier*sd))
        bandLower.append(sma[i-period]- (multiplier*sd))
        i=i+1


    return {"mid": bandMid, "upper": bandUpper, "lower": bandLower}


def update_companies():
    global companyList
    global updatedAt
    # print("\nUpdating Companies List... \n")

    with open('companies.json', 'r+') as outfile:
        x = json.loads(outfile.read())
        companyList = x["content"]
        updatedAt = x["updatedAt"]

    print("\nUpdated at  \n....\n"+str(updatedAt))


if __name__ == '__main__':
    update_companies()
    analyzeBollingerBands()
