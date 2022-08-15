import json
import datetime
import time
from scripts import SendMessage

companyList = []
newCompanyList = []
companyData = {}
dailyjsonData = {}

updatedAt=0.0

def analyzeRSI():
    today = datetime.datetime(datetime.datetime.utcnow().year,
                              datetime.datetime.utcnow().month,
                              datetime.datetime.utcnow().day,0,0,0).replace(tzinfo= datetime.timezone.utc).timestamp()
    print("today's gmt epoch "+str(today))

    stochData = {}
    companyName = "EIC"
    buylist = {}
    selllist = {}

    with open('alldata.json', 'r+') as outfile:
        global updatedAt
        print("Reading all Data")
        allData = json.loads(outfile.read())
        print("Reading all Data done")
        print(companyList)
        for companyName in companyList:
            try:
                if (updatedAt != datetime.datetime.fromtimestamp(time.mktime(time.gmtime(
                    allData[companyName]["data"]["t"][len(allData[companyName]["data"]["t"]) - 1]))).strftime("%Y-%m-%d")):

                    print(str(companyName) + " has not been traded for " + str(updatedAt)+" but at "+str(datetime.datetime.fromtimestamp(time.mktime(time.gmtime(
                    allData[companyName]["data"]["t"][len(allData[companyName]["data"]["t"]) - 1]))).strftime("%Y-%m-%d")))
                    continue

                stochData = getStochRSI(data= allData[companyName]["data"], span=10, periodRSI= 42, period= 42, smoothK= 5, smoothD= 5)
                if stochData != -1:
                    print("Evaluating "+companyName)
                    if getConvergenceStochastic(stochData= stochData, timeSpan= 3):
                        buylist[companyName]= stochData["stochRSIK"][len(stochData["stochRSIK"])-1]
                    if getDivergenceStochastic(stochData= stochData, timeSpan= 3):
                        selllist[companyName]= stochData["stochRSIK"][len(stochData["stochRSIK"])-1]

            except:
                continue

    buylist = {k: v for k, v in sorted(buylist.items(), key=lambda item: item[1])}
    selllist = {k: v for k, v in sorted(selllist.items(), key=lambda item: item[1], reverse= True)}

    print("Buy the following scripts : \n")
    for c in buylist:
        print(c)
    print("\n\nSell the following scripts : \n")
    for c in selllist:
        print(c)

    SendMessage.send_StochasticRSI_message(buylist, selllist)

    with open('buyData.json', 'w+') as outfile:
        json.dump(buylist, outfile, indent=4)

    with open('sellData.json', 'w+') as outfile:
        json.dump(selllist, outfile, indent=4)


def getConvergenceStochastic(stochData, timeSpan):
    t = timeSpan

    c = len(stochData["stochRSID"])-timeSpan
    d = []
    while (c < len(stochData["stochRSID"])):
        d.append(stochData["stochRSID"][c] - stochData["stochRSIK"][c])
        c = c + 1

    # timeSeries = allData[companyName]["data"]["t"]
    # while (c <= len(d)):

    x = d[-t: len(d)]
    srtX = sorted(x, reverse=True)
    if (x == srtX):
        # print(x)
        if (8 > d[len(d)-1]):
            # print(d[len(d) - t])
            # print(d[len(d) - 1])
            # print("Buy signal at " + str(t))#str(datetime.datetime.fromtimestamp(timeSeries[len(timeSeries) - len(d) + c - 1]).strftime('%Y-%m-%d')))
            print(x)
            return True
        # c = c + 1
    return False


def getDivergenceStochastic(stochData, timeSpan):
    t = timeSpan

    c = len(stochData["stochRSID"])-timeSpan
    d = []
    while (c < len(stochData["stochRSID"])):
        d.append(stochData["stochRSID"][c] - stochData["stochRSIK"][c])
        c = c + 1

    # timeSeries = allData[companyName]["data"]["t"]
    # while (c <= len(d)):

    x = d[-t: len(d)]
    srtX = sorted(x, reverse=False)
    if (x == srtX):
        # print(x)
        if (-8 < d[len(d)-1]):
            # print(d[len(d) - t])
            # print(d[len(d) - 1])
            # print("Buy signal at " + str(t))#str(datetime.datetime.fromtimestamp(timeSeries[len(timeSeries) - len(d) + c - 1]).strftime('%Y-%m-%d')))
            print(x)
            return True
        # c = c + 1
    return False

def getGainAndLoss(data):
    gains = []
    losses = []
    i=0
    while i<len(data)-1:
        if data[i]<data[i+1]:
            gains.append(data[i+1]-data[i])
            # print("gain of "+str(data[i+1]-data[i]))
            losses.append(0)
        if data[i]>data[i+1]:
            losses.append(data[i]-data[i+1])
            # print("loss of "+str(data[i]-data[i+1]))
            gains.append(0)
        if data[i]==data[i+1]:
            gains.append(0)
            losses.append(0)
        i=i+1
    return {"gains": gains, "losses":losses}


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
        print("No enough data to calculate wilder's ema")
        return -1

    ema= []
    c = period
    while c <= len(data):
        ema.append(sum(data[c-period:c])/period)
        c=c+1
    return ema


def getRSI(data, span= 14, period= 14):
    x = period + span
    length = len(data["c"])
    if  length < x:
        print("data not enough")
        return -1

    gains = getGainAndLoss(data["c"])["gains"]
    losses = getGainAndLoss(data["c"])["losses"]

    emaGain= get_ema_wilder(gains, period)
    emaLoss= get_ema_wilder(losses, period)


    rsi= []
    i= 0
    while i< len(emaGain):
        # print("Date : "+str(datetime.datetime.fromtimestamp((data["t"][len(data["t"])-i-1])).strftime('%Y-%m-%d')))
        rsi.insert(0, 100 - ((emaLoss[len(emaLoss) - i - 1] * 100 )/ (emaGain[len(emaLoss) - i - 1] + emaLoss[len(emaLoss) - i - 1])))
        # print("\t\t\t\trsi = "+ str(rsi[0]))
        i=i+1

    return rsi


def getStochRSI(data, span= 10, periodRSI= 14, period= 14, smoothK= 3, smoothD= 3):
    stochRsiPre = []
    rsi= getRSI(data, span, periodRSI)

    if rsi == -1:
        return -1

    i= period
    while i<= (len(rsi)):
        stochRsiPre.append(((rsi[i-1] - min(rsi[i-period: i])) * 100) / (max(rsi[i-period: i]) - min(rsi[i-period: i])))
        # print("Date : "+str(datetime.datetime.fromtimestamp((data["t"][len(data["t"])-len(rsi)+i])).strftime('%Y-%m-%d')))
        # print("\t\t\t\tstoch rsi = "+ str(stochRsi[len(stochRsi)-1]))
        i=i+1

    stochRSIK = get_sma(stochRsiPre, smoothK)
    stochRSID = get_sma(stochRSIK, smoothD)


    stochRSIK = stochRSIK[(len(stochRSIK)-len(stochRSID)):len(stochRSIK)]

    return {"rsi": rsi, "stochRSIK": stochRSIK, "stochRSID": stochRSID}


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
    analyzeRSI()
