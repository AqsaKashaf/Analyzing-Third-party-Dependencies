

import sys, tldextract
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import numpy as np
import itertools, random

# QuoVadisTrustlinkBV: QuoVadisLimited

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (13,9)
plt.rcParams["axes.labelsize"] = 40
plt.rcParams["axes.titlesize"] =  30
plt.rcParams["lines.linewidth"] = 3
plt.rcParams["xtick.labelsize"] = 40
plt.rcParams["ytick.labelsize"] = 40
plt.rcParams["legend.fontsize"] = 30

def autolabel(rects,ax):
    for rect in rects:
        h = rect.get_height()
        ax.annotate("{0:.1f}".format(h).lstrip('0'),
                    xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext = (0,3),
                    textcoords="offset points",
                    ha="center", va="bottom", size=28, rotation=90)

def plotWebsiteStats(stats,total):

    labels = [100*(10**r) for r in range(4)]

    x = np.arange(len(labels))
    # print(x)
    width = 0.15

    fig, ax = plt.subplots()
    
    # ex16 = [len(stats[k][f"exclusive{prefix}"])/k for k in labels]
    # print(ex16)
    patterns = [ "|||" , "\\\\" , "/" , "+" , "-", "..", "**","x", "oo", "O" ]
    https = [len(stats[k][f"https"])/k*100 for k in labels]

    third = [len(stats[k][f"third"])/k*100 for k in labels]

    stapled =  [len(stats[k][f"stapled"])/k*100 for k in labels]

    # exclusive = [len(stats[k][f"exclusive"])/total[k] for k in labels]

    # third_pvt = [len(stats[k][f"third-pvt"])/total[k] for k in labels]

    # third_third = [len(stats[k][f"third-third"])/total[k] for k in labels]

    r1 = ax.bar(x-width*1.5, https, width, label="HTTPS Support",hatch=patterns[0],color='white', edgecolor='black')

    r2 = ax.bar(x-width/2, third, width, label="Third Party Dependency",hatch=patterns[1],color='white', edgecolor='black')

    r3 = ax.bar(x+width/2, stapled, width, label="Support for OCSP Stapling",hatch=patterns[3],color='white', edgecolor='black')

    # r3 = ax.bar(x+width/2, redundant, width, label="Redundant")

    # r4 = ax.bar(x+width*1.5, third_third, width, label="Third + Third Redundancy")
    # r5 = ax.bar(x+width*2.5, third_pvt, width, label="Third + Pvt Redundancy")

    ax.set_ylabel("Percentage of websites")

    ax.set_xlabel("Alexa Rank")

    ax.set_xticks(x)

    ax.set_xticklabels(labels)

    lgd = ax.legend(bbox_to_anchor=(0.5,1.35),loc="upper center",ncol=2)
    autolabel(r1,ax)
    autolabel(r2,ax)
    autolabel(r3,ax)
    # autolabel(r4,ax)
    # autolabel(r5,ax)
    # fig.tight_layout()

    plt.savefig(f"figures/webStatsCA2020.pdf", bbox_extra_artists=(lgd,), bbox_inches='tight')


# def readCAMap(filename):
#     f = open(filename,"r")
#     CA_MAP = {}
#     for line in f:
#         line = line.strip().split(",")
#         ca = line[0]
#         urls = set(line[1].split(":"))
#         if(ca not in CA_MAP):
#             CA_MAP[ca] = set()


def plotTopConcentration(topk,rank, total, prefix):

    labels = topk

    x = np.arange(len(labels))
    width = 0.5

    fig,ax = plt.subplots()

    concentration = []
    # risk = []
    for k,count in topk.items():
       
        concentration.append(count/total[rank])
        # risk.append(dataEx[k][int(math.log10(rank) - 2)]/total[rank])

    
    # r = []
    # for p,c in concentration.items():
    r=ax.bar(x-width/2, concentration, width)
    # rEx = ax.bar(x+width/2,risk,width)

    ax.set_ylabel("Fraction  of Websites")

    ax.set_xlabel("Providers")

    ax.set_xticks(x)

    ax.set_xticklabels(labels,rotation=40,ha="right")
    # lgd = ax.legend(bbox_to_anchor=(0.5,1.3),loc="upper center",ncol=2)
    # for rect in r:
    autolabel(r,ax)
    # autolabel(rEx,ax)
    
    plt.savefig(f"figures/provider_{prefix}_{rank}.pdf",bbox_inches='tight')

def plotTopConcRisk(topk,riskValues, rank, total, prefix):

    labels = topk

    x = np.arange(len(labels))
    width = 0.35

    fig,ax = plt.subplots()

    concentration = []
    risk = []
    for k,count in topk.items():
       
        concentration.append(count/total[rank])
        risk.append(riskValues[k]/total[rank])

    
    # r = []
    # for p,c in concentration.items():
    r=ax.bar(x-width/2, concentration, width, label="Provider Concentration")
    rEx = ax.bar(x+width/2,risk,width, label="Provider Impact")

    ax.set_ylabel("Fraction  of Websites")

    ax.set_xlabel("Providers")

    ax.set_xticks(x)

    ax.set_xticklabels(labels,rotation=40,ha="right")
    lgd = ax.legend(bbox_to_anchor=(0.5,1.15),loc="upper center",ncol=2)
    # for rect in r:
    autolabel(r,ax)
    autolabel(rEx,ax)
    
    plt.savefig(f"figures/provider_{prefix}_{rank}.pdf",bbox_extra_artists=(lgd,),bbox_inches='tight')
    # , bbox_extra_artists=(lgd,), 


CA_MAP = {"SECOMTrustSystemsCO.LTD.":"secomtrust.net", "NijimoInc.":"secomtrust.net", "NationalInstituteofInformatics":"secomtrust.net", "Agenziaperl'ItaliaDigitale":"agid.gov.it","CrossTrust":"crosstrust.net","JapanRegistryServicesCo.Ltd.":"jprs.jp"}

def majorProviders(third,urlData, rank, URL_CA_MAP):

    providerFrq = {}
    for (r,w), providers in third.items():
        if(r <= rank):
            providers  = urlData[(r,w)]
            if(len(providers)==0):
                ca = list(third[(r,w)])[0]
                # print(r,w)
                providers.add(CA_MAP[ca])
            for p in providers:
                p = tldextract.extract(p)
                p = p.domain + "." + p.suffix
                # print(p)
                p = URL_CA_MAP[p]
                if(p not in providerFrq):
                    providerFrq[p] = set()
                providerFrq[p].add((r,w))

    provider_count = {}
    for pid, websites in providerFrq.items():
        provider_count[pid] = len(websites)

    provider_count = {k: v for k, v in sorted(provider_count.items(), key=lambda item: item[1], reverse=True)}
    return providerFrq, provider_count

def majorRiskyProviders(third,urlData, rank, stapled, URL_CA_MAP):

    providerFrq = {}
    for (r,w), providers in third.items():
        if(r <= rank):
            providers = urlData[(r,w)]
            if(len(providers)==0):
                ca = list(third[(r,w)])[0]
                # print(r,w)
                providers.add(CA_MAP[ca])
            for p in providers:
                p = tldextract.extract(p)
                p = p.domain + "." + p.suffix
                p = URL_CA_MAP[p]
                if(p not in providerFrq):
                    providerFrq[p] = set()
                if((r,w) not in stapled):
                    providerFrq[p].add((r,w))

    provider_count = {}
    for pid, websites in providerFrq.items():
        provider_count[pid] = len(websites)

    provider_count = {k: v for k, v in sorted(provider_count.items(), key=lambda item: item[1], reverse=True)}
    return providerFrq, provider_count



def findHTTPS(data,rank):
    websites = set()
    for (r,w), cas in data.items():
        if(r <= rank):
            websites.add((r,w))

    return websites

def findOCSP(data,rank):
    websites = set()
    for (r,w), cas in data.items():
        if(r <= rank and len(cas) > 0):
            websites.add((r,w))

    return websites

def findCRL(data,rank):
    websites = set()
    for (r,w), cas in data.items():
        if(r <= rank and len(cas) > 0):
            websites.add((r,w))

    return websites

def findThird(data,rank):
    websites = set()
    for (r,w), cas in data.items():
        if(r <= rank):
            websites.add((r,w))

    return websites


def findStapledThird(third, stapleData, rank):

    websites = set()

    for (r,w),ca in third.items():
        if(r <= rank and (r,w) in stapleData):
            websites.add((r,w))
    
    return websites


def readStapleData(filename):
    f = open(filename,"r")
    data = set()
    for line in f:
        line = line.strip().split(",")
        rank = int(line[0])
        if(rank <= 100000):
            website = line[1]
            staple = line[2]
            if(staple == "yes"):
                data.add((rank,website))
    return data
    
def readData(filename):

    f = open(filename,"r")
    data = {}
    for line in f:
        line = line.strip().split(",")
        rank = int(line[0])
        if(rank <= 100000):
            website = line[1]
            # data[(rank,website)] = line[2]
            values = set(line[2].split(" "))
            values.discard("none")
            if((rank, website) not in data):
                data[(rank,website)] = set()
            data[(rank,website)] = data[(rank,website)].union(values)
    
    duals = set()
    for (r,w),cas in data.items():
        if(len(cas) > 1):
            duals.add((r,w))
        
        # print("duals", len(duals),filename
        
    return data, duals

def generateDetails(data, filename):

    details = {}
    duals = set()
    f = open(filename,"r")
    for line in f:
        line = line.strip().split(",")
        # print( line)
        values = line[2].split(" ")
        for value in values:
            value = tldextract.extract(value)
            value = value.domain + "." + value.suffix
            rank = int(line[0])
            w = line[1]
            try:
                ca = data[(rank,w)]
                ca = list(ca)[0]
                if(ca not in details):
                    details[ca] = set()
                details[ca].add(value)
            except KeyError:
                if(rank <= 100000):
                    duals.add(rank)
    
    # print(len(duals))
    return details



def uniqueCA(data):

    unique = set()
    for (r,w), cas in data.items():
        if(len(cas) > 1): 
            # print(r,w,",".join(cas))
            pass
        # for ca in cas:
            # tldCA = tldextract.extract(ca)
            # tldCA = tldCA.domain + "." + tldCA.suffix
            # unique.add(tldCA.rstrip("."))
        unique.add(ca)
    return unique

def findTotal(data):
    total = {}
    total[100] = set()
    total[1000] = set()
    total[10000] = set()
    total[100000] = set()

    for (i,j),k in data.items():
        if(len(k) > 0):
            if(i <= 100):
                total[100].add(i)
            
            if(i <= 1000):
                total[1000].add(i)
            
            if(i <= 10000):
                total[10000].add(i)
            
            if(i <= 100000):
                total[100000].add(i)
    
    frequency = {k:len(v) for k,v in total.items()}
    return total, frequency

def deleteDuals(data,duals):
    for d in duals:
        del data[d]
    return data



def readCAMap(filename):
    f = open(filename,"r")
    urlca = {}
    for line in f:
        # print(line)
        line= line.strip().split(" ")
        url = line[0]
        ca = line[1]
        urlca[url] = ca
    
    return urlca

def main():

    caFile = sys.argv[1]
    stapleFile = sys.argv[2]
    stapleData = readStapleData(stapleFile)
    # print(len(stapleData))
    data,duals = readData(caFile)
    data = deleteDuals(data, duals)


    urlData,_ = readData("CA_URL_CURRENT")
    urlData = deleteDuals(urlData, duals)

    URL_CA_MAP = readCAMap("url-ca-map")

    third,_ = readData("third")

    allSamples = {}
    random.seed(10)
    for (r,w),cdns in data.items():
        if(len(cdns) > 0):
            allSamples[r] = w
    
    ranks = list(allSamples.keys())
    random.shuffle(ranks)
    idxs = ranks[:100]

    # for r in idxs:
    #     w = allSamples[r]
    #     url = urlData[(r,w)]
    #     if(len(url)>0):
    #         p = tldextract.extract(list(url)[0])
    #         url = p.domain + "." + p.suffix
    #         p = URL_CA_MAP[url]
    #         print(r, w, p, url)

    # for (r,w),_ in third.items():
    #     # print(r,w)
    #     url = urlData[(r,w)]
    #     if(len(url)>0):
    #         p = tldextract.extract(list(url)[0])
    #         p = p.domain + "." + p.suffix
    #         p = URL_CA_MAP[p]
    #         # ca = URL_CA_MAP[list(url)[0]]
    #         print(f"{r},{w},{p}")

    # 


    ocsp,_ = readData("OCSP_CURRENT")
    ocsp = deleteDuals(ocsp, duals)
    crl,_ = readData("CRL_CURRENT")
    crl = deleteDuals(crl, duals)
    pvt = readData("pvt")

    # print(len(data), len(third), len(ocsp), len(crl))

    webStats = {}
    totalwebsites, totalCount = findTotal(data)
    
    provider_count = {}
    provider_risk = {}
    provider_websites = {}
    # print(totalCount)

    for r in range(4):
        rank = 100*(10**r)
        webStats[rank] = {}
        webStats[rank]["https"] = findHTTPS(data, rank)
        webStats[rank]["third"] = findThird(third, rank)
        webStats[rank]["ocsp"] = findOCSP(ocsp, rank)
        webStats[rank]["crl"] = findCRL(crl, rank)
        webStats[rank]["stapled"] = findStapledThird(third, stapleData, rank)
        webStats[rank]["stapledAll"] = findStapledThird(data, stapleData, rank)
        # print(len(webStats[rank]["ocsp"]))
        # , sorted(webStats[rank]["crl"]))

        provider_websites[rank], provider_count[rank] = majorProviders(third, urlData, rank, URL_CA_MAP)
        # provider_websites[rank], provider_count[rank] = majorProviders(data, urlData, rank, URL_CA_MAP)

        top10 = dict(itertools.islice(provider_count[rank].items(), 10))
        plotTopConcentration(top10, rank, totalCount,"concCA")

        provider_websites[rank], provider_risk[rank] = majorRiskyProviders(third, urlData,rank,webStats[rank]["stapled"], URL_CA_MAP)
        # provider_websites[rank], provider_risk[rank] = majorRiskyProviders(data, urlData,rank,webStats[rank]["stapledAll"], URL_CA_MAP)
        top10risk = dict(itertools.islice(provider_risk[rank].items(),10))
        # print(top10risk)
        # plotTopConcentration(top10risk, rank, totalCount,"riskCA")
        top5 = dict(itertools.islice(provider_count[rank].items(), 5))
        # plotTopConcRisk(top5, provider_risk[rank], rank, totalCount,"conc-risk-CA")


    plotWebsiteStats(webStats,totalCount)

    # print(len(webStats[100000]["third"]))
    # print(len(webStats[100000]["stapled"]))
    # print(len(provider_risk[100000]))
    
    # for provider, websites in provider_websites[100000].items():
    #     websites = [str(r) + "-" + w for r,w in websites]
    #     websites = ":".join(websites)
    #     print(f"{provider},{websites}")

if __name__ == "__main__":
    main()