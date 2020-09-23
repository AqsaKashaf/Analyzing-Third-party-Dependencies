import sys 
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import numpy as np
import itertools, random


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
                    xytext = (1,3),
                    textcoords="offset points",
                    ha="center", va="bottom", size=26, rotation=90)

def plotWebsiteStats(stats,total):

    labels = [100*(10**r) for r in range(4)]

    x = np.arange(len(labels))
    # print(x)
    width = 0.15
    patterns = [ "|||" , "\\\\" , "/" , "+" , "-", "..", "**","x", "oo", "O" ]
    fig, ax = plt.subplots()
    
    # ex16 = [len(stats[k][f"exclusive{prefix}"])/k for k in labels]
    # print(ex16)
    third = [len(stats[k][f"third"])/total[k]*100 for k in labels]

    redundant =  [len(stats[k][f"redundant"])/total[k]*100 for k in labels]

    exclusive = [len(stats[k][f"exclusive"])/total[k]*100 for k in labels]

    third_pvt = [len(stats[k][f"third-pvt"])/total[k]*100 for k in labels]

    third_third = [len(stats[k][f"third-third"])/total[k]*100 for k in labels]

    # r1 = ax.bar(x-width*1.5, ex16, width, label="Exclusive Dependency")

    r1 = ax.bar(x-width*1.5, third, width, label="3rd Party Dependency", hatch=patterns[0],color='white', edgecolor='black')

    r2 = ax.bar(x-width/2, exclusive, width, label="Critical Dependency",hatch=patterns[1],color='white', edgecolor='black')

    r3 = ax.bar(x+width/2, redundant, width, label="Redundancy", hatch=patterns[3],color='white', edgecolor='black')

    r4 = ax.bar(x+width*1.5, third_third, width, label="muliple 3rd",hatch=patterns[5],color='white', edgecolor='black')
    # r5 = ax.bar(x+width*2.5, third_pvt, width, label="3rd + Pvt")

    ax.set_ylabel("Percentage of websites")

    ax.set_xlabel("Alexa Rank")

    ax.set_xticks(x)

    ax.set_xticklabels(labels)

    lgd = ax.legend(bbox_to_anchor=(0.5,1.35),loc="upper center",ncol=2)
    autolabel(r1,ax)
    autolabel(r2,ax)
    autolabel(r3,ax)
    autolabel(r4,ax)
    # autolabel(r5,ax)
    # fig.tight_layout()

    plt.savefig(f"figures/webStatsCDN2020.pdf", bbox_extra_artists=(lgd,), bbox_inches='tight')

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

def findCDN(data,rank):
    websites = set()
    for (r,w), cdns in data.items():
        if(r <= rank and len(cdns) > 0):
            websites.add((r,w))

    return websites

def findThird(data,rank):
    websites = set()
    for (r,w), cdns in data.items():
        if(r <= rank):
            websites.add((r,w))

    return websites


def readData(filename):

    data = {}
    f = open(filename,"r")
    for line in f:
        line = line.strip().split(",")
        rank = int(line[0])
        if(rank <= 100000):
            website = line[1]
            provider = line[2].lower()
            key = rank,website
            if(key not in data):
                data[key] = set()
            if(provider != "none"):
                data[key].add(provider)
    
    return data

def findExclusive(data, rank):
    exclusive = set()
    redundant = set()
    for (r,w), providers in data.items():
        if(r <= rank):
            if(len(data[(r,w)]) == 1):
                exclusive.add((r,w))
            elif(len(data[(r,w)]) > 1):
                redundant.add((r,w))
        
    return redundant,exclusive

def findExclusiveThird(third, data, rank):
    exclusive = set()
    redundant = set()
    for (r,w), providers in third.items():
        if(r <= rank):
            if(len(data[(r,w)]) == 1):
                exclusive.add((r,w))
            elif(len(data[(r,w)]) > 1):
                redundant.add((r,w))
        
    return redundant,exclusive

def findPvtThird(redundant,third, pvt):
    websites = set()
    for i in redundant:
        if i in third and i in pvt:
            websites.add(i)
    
    return websites

def findThirdThird(redundant, third, pvt):
    websites = set()

    for i in redundant:
        if i in third and i not in pvt:
            websites.add(i)
    
    return websites



def majorProviders(data, rank):

    providerFrq = {}
    for (r,w), providers in data.items():
        if(r <= rank):
            for p in providers:
                if(p not in providerFrq):
                    providerFrq[p] = set()
                providerFrq[p].add((r,w))

    provider_count = {}
    for pid, websites in providerFrq.items():
        provider_count[pid] = len(websites)

    provider_count = {k: v for k, v in sorted(provider_count.items(), key=lambda item: item[1], reverse=True)}
    return providerFrq, provider_count

def majorRiskyProviders(data, rank, redundant):

    providerRisk = {}
    for (r,w), providers in data.items():
        if(r <= rank):
            for p in providers:
                if(p not in providerRisk):
                    providerRisk[p] = set()
                if((r,w) not in redundant):
                    providerRisk[p].add((r,w))

    provider_count = {}
    for pid, websites in providerRisk.items():
        provider_count[pid] = len(websites)

    provider_count = {k: v for k, v in sorted(provider_count.items(), key=lambda item: item[1], reverse=True)}
    return providerRisk, provider_count


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


def findCDNs(data):
    cdns = set()
    for (r,w),p in data.items():
        for cdn in p:
            cdns.add(cdn)
    
    return cdns, len(cdns)
def main():

    filename = sys.argv[1]

    exCDNS = ['rapleaf', 'staticfile', 'pantheon', 'jquerycdn', 'upai', 'sirv', 'cdnjs', 'tinycdn', 'cloudinary', 'anothercloud', 'unpkg', 'keycdn', 'swiftserve', 'zenedge', 'uploadcare','maxcdn', 'stackpath', 'azion', 'jsdelivr', 'netlify', 'chinanetcenter', 'fastly', 'distilnetworks', 'telefonica', 'twitter', 'bootstrapcdn', 'telenor', 'kinxcdn', 'pagecdn', 'turbobytes', 'ntt']

    data = readData(filename)

    third = readData("newThird")
    pvt = readData("newPvt")

    # for (r,w),_ in third.items():
    #     providers = data[(r,w)]
    #     for p in providers:
    #         print(f"{r},{w},{p}")

    allSamples = {}
    random.seed(10)
    for (r,w),cdns in data.items():
        if(len(cdns) > 0):
            allSamples[r] = w
    
    ranks = list(allSamples.keys())
    random.shuffle(ranks)
    idxs = ranks[:100]

    # for r in idxs:
    #     print(r, allSamples[r], ",".join(data[(r, allSamples[r])]))
    


    # thirdcdn = ["cloudflare","fastly","tencent","unpkg","jsdelivr","cdnjs"]
    # for (i,j),k in data.items():
    #     for cdn in k:
    #         if(i,j) not in third and cdn not in thirdcdn:
    #             print(f"{i},{j},{cdn}")
    #         # if cdn in thirdcdn:


    

    # print(findCDNs(data))

    # print(len(data), len(third))

    webStats = {}
    totalwebsites, totalCount = findTotal(data)
    provider_count = {}
    provider_risk = {}
    provider_websites = {}
    print(totalCount)

    for r in range(4):
        rank = 100*(10**r)
        # print (rank)
        webStats[rank] = {}
        webStats[rank]["cdn"] = findCDN(data, rank)
        webStats[rank]["third"] = findThird(third, rank)
        webStats[rank]["redAll"], webStats[rank]["excAll"] = findExclusive(data, rank)
        webStats[rank]["redundant"], webStats[rank]["exclusive"] = findExclusiveThird(third, data, rank)
        webStats[rank]["third-pvt"] = findPvtThird(webStats[rank]["redundant"],third,pvt)
        webStats[rank]["third-third"] = findThirdThird(webStats[rank]["redundant"], third, pvt)
        _, provider_count[rank] = majorProviders(third, rank)

        # provider_websites[rank],_ = majorProviders(data,rank) 
        # provider_websites[rank],_ = majorProviders(third,rank) 

        # _, provider_risk[rank] = majorRiskyProviders(third,rank,webStats[rank]["redundant"])
        # _, provider_risk[rank] = majorRiskyProviders(data,rank,webStats[rank]["redAll"])

        # provider_websites[rank], provider_risk[rank] = majorRiskyProviders(data,rank,webStats[rank]["redAll"])

        provider_websites[rank], provider_risk[rank] = majorRiskyProviders(third,rank,webStats[rank]["redundant"])
        top10 = dict(itertools.islice(provider_count[rank].items(), 10))
        top10risk = dict(itertools.islice(provider_risk[rank].items(),10))
        # plotTopConcentration(top10, rank, totalCount,"concCDN")
        # plotTopConcentration(top10risk, rank, totalCount,"riskCDN")
        top5 = dict(itertools.islice(provider_count[rank].items(), 5))
        print(top10risk)
        # plotTopConcRisk(top5, provider_risk[rank], rank, totalCount,"conc-risk-cdn")


    plotWebsiteStats(webStats,totalCount)

    # print(len(webStats[100000]["third"]))
    # print(len(webStats[100000]["exclusive"]))
    # print(len(provider_risk[100000]))



    # for provider, websites in provider_websites[100000].items():
    #     websites = [str(r) + "-" + w for r,w in websites]
    #     websites = ":".join(websites)
    #     print(f"{provider},{websites}")


    # print(len(webStats[100]["redAll"]),webStats[100]["redAll"])
    # print(len(webStats[100]["redundant"]),webStats[100]["redundant"])

    # for cdn in exCDNS:
    #     try:
    #         print(cdn, provider_risk[100000][cdn], totalCount[100000])
    #     except KeyError:
    #         print(cdn)

if __name__ == "__main__":
    main()