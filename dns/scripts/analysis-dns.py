

import sys
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import numpy as np
import itertools, random

#q1: if the website use third party or not (ranking wise)
#q2: if the website is redundant or not
    #q2.1: redundancy with pvt and third
    #q2.2: redundancy with thirds
#q3: major providers across ranks
#q4: major risky providers across ranks


#q5: trends across organizations, (organizations that have separate infrastructure for their own domains and offer same service to other domains like google.com, googledomains.com, etc.)
    #q5.1: concentration across organizations, your own domains and the domains you serve
    #q5.2: redundancy across organizations wrt their own domains, wrt domains they serve
# providers that have their own infrastructure but use third party for their own domains like amazon



DNS_GROUP_FILE = "./newGroups"

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
        ax.annotate("{0:.2f}".format(h).lstrip('0'),
                    xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext = (0,3),
                    textcoords="offset points",
                    ha="center", va="bottom", size=30)

def plotWebsiteStats(stats,total):

    labels = [100*(10**r) for r in range(4)]

    x = np.arange(len(labels))
    # print(x)
    width = 0.15

    fig, ax = plt.subplots()
    
    # ex16 = [len(stats[k][f"exclusive{prefix}"])/k for k in labels]
    # print(ex16)
    third = [len(stats[k][f"third"])/total[k] for k in labels]

    redundant =  [len(stats[k][f"redundant"])/total[k] for k in labels]

    exclusive = [len(stats[k][f"exclusive"])/total[k] for k in labels]

    third_pvt = [len(stats[k][f"third-pvt"])/total[k] for k in labels]

    third_third = [len(stats[k][f"third-third"])/total[k] for k in labels]

    # r1 = ax.bar(x-width*1.5, ex16, width, label="Exclusive Dependency")

    r1 = ax.bar(x-width*1.5, third, width, label="3rd Party Dependency")

    r2 = ax.bar(x-width/2, exclusive, width, label="3rd Party Exclusive Dependency")

    r3 = ax.bar(x+width/2, redundant, width, label="Redundant")

    r4 = ax.bar(x+width*1.5, third_third, width, label="3rd + 3rd")
    r5 = ax.bar(x+width*2.5, third_pvt, width, label="3rd + Pvt")

    ax.set_ylabel("Fraction of websites")

    ax.set_xlabel("Alexa Rank")

    ax.set_xticks(x)

    ax.set_xticklabels(labels)

    lgd = ax.legend(bbox_to_anchor=(0.5,1.35),loc="upper center",ncol=2)
    autolabel(r1,ax)
    autolabel(r2,ax)
    autolabel(r3,ax)
    autolabel(r4,ax)
    autolabel(r5,ax)
    # fig.tight_layout()

    plt.savefig(f"figures/webStats2020.pdf", bbox_extra_artists=(lgd,), bbox_inches='tight')


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
    lgd = ax.legend(bbox_to_anchor=(0.5,1.3),loc="upper center",ncol=2)
    # for rect in r:
    autolabel(r,ax)
    # autolabel(rEx,ax)
    
    plt.savefig(f"figures/provider_{prefix}_{rank}.pdf",bbox_inches='tight')
    # , bbox_extra_artists=(lgd,), 
    
def plotTopConcRisk(topk,riskValues, rank, total, prefix):

    labels = topk

    x = np.arange(len(labels))
    width = 0.35

    fig,ax = plt.subplots()

    concentration = []
    risk = []
    for k,count in topk.items():
       
        # concentration.append(count/total[rank])
        concentration.append(count/rank)

        # risk.append(riskValues[k]/total[rank])
        risk.append(riskValues[k]/rank)

    
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


def findThird(third,rank):

    websites = set()
    for (r,w), providers in third.items():
        if(r <= rank):
            websites.add(r)
    return websites


def findExclusiveThird(third, data, rank, groupMAP):
    exclusive = set()
    redundant = set()
    for (r,w), providers in third.items():
        if(r <= rank):
            if(len(data[(r,w)]) == 1):
                exclusive.add((r,w))
            else:
                grps = set()
                for p in providers:
                    try:
                        grps.add(groupMAP[p])
                    except KeyError:
                        grps.add(p)              
                if(len(grps) > 1):
                    redundant.add((r,w))
                else:
                    exclusive.add((r,w))
        
    return redundant,exclusive

def findPvtThird(redundant, third, pvt):
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

def majorProviders(data, rank, groupMAP):

    providerFrq = {}
    for (r,w), providers in data.items():
        if(r <= rank):
            for p in providers:
                try:
                    grpid = groupMAP[p]
                    if(grpid not in providerFrq):
                        providerFrq[grpid] = set()
                    providerFrq[grpid].add((r,w))
                except KeyError:
                    if(p not in providerFrq):
                        providerFrq[p] = set()
                    providerFrq[p].add((r,w))

    provider_count = {}
    for pid, websites in providerFrq.items():
        provider_count[pid] = len(websites)

    provider_count = {k: v for k, v in sorted(provider_count.items(), key=lambda item: item[1], reverse=True)}
    return providerFrq, provider_count

def majorRiskyProviders(data, rank, groupMAP,redundant):

    providerRisk = {}
    for (r,w), providers in data.items():
        if(r <= rank):
            for p in providers:
                try:
                    grpid = groupMAP[p]
                    if(grpid not in providerRisk):
                        providerRisk[grpid] = set()
                    if((r,w) not in redundant):
                        providerRisk[grpid].add((r,w))
                except KeyError:
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

def readData(filename, uncategorized):

    data = {}
    f = open(filename,"r")
    for line in f:
        line = line.strip().split(",")
        rank = int(line[0])
        if(rank <= 100000):
            website = line[1]
            if(website not in uncategorized):
                ns = line[2].lower()
                if(ns in "nxdomain"):
                    ns = "NXDOMAIN"
                key = rank,website
                if(key not in data):
                    data[key] = set()

                data[key].add(ns)
    
    return data

def readGroups():
    f = open(DNS_GROUP_FILE,"r")
    groups = {}
    groupMap = {}
    uid = 0
    for line in f:
        line = line.strip().split(" ;;; ")
        grpId = line[0].lower() 
        
        if (grpId in groups):
            grpId += str(uid)
            print(grpId)
            uid+=1
        entries = line[1].split(" ")
        # if("dynect.com" in entries):
        #     grpId = "Dynect"
        # # elif("ultradns.net" in entries):
        # #     grpId = "UltraDNS"
        # # elif("awsdns-58.com" in entries):
        # #     grpId = "AWS DNS"
        # # elif("nsone.net" in entries):
        # #     grpId = "NS1"
        # # elif("dnsv5" in entries):
        # #     grpId = "DNSPod"
        # # elif("dnsmadeeasy.com" in entries):
        # #     grpId = "DNSMadeEasy"

        groups[grpId] = entries
        for p in groups[grpId]:
            groupMap[p] = grpId
        
       
        
        # if(isinstance(grpId,int)):
        #     grpId+= 1
    
    f.close()
    return groups, groupMap


def readUncategorized():
    uncat = set()
    f = open("uncategorized", "r")
    for line in f:
        line = line.strip()
        uncat.add(line.lower())

    f.close()
    return uncat



def attachRank():
    f = open("../list1m2020.csv","r")
    rank = 1
    data = {}
    for line in f:
        line = line.strip()        
        data[rank] = line
        rank += 1
    
    return data



def main():

    filename = sys.argv[1]
    uncategorized = readUncategorized()

    groupIDs, groupMAP = readGroups()

    data = readData(filename, uncategorized)
    third = readData("third", uncategorized)

    ranks = attachRank()
    random.seed(10)
    idxs = list(range(100000))
    random.shuffle(idxs)
    idxs = idxs[:150]

    for i in idxs:
        website = ranks[i]
        if((i,website) in data):
            print(i, website, ",".join(data[(i,website)]))

    # for (r,w), providers in third.items():
    #     for p in providers:
    #         try:
    #             grpid = groupMAP[p]
    #             print(f"{r},{w},{grpid}")
    #         except KeyError:
    #             print(f"{r},{w},{p}")
                

    # third = readData("third", uncategorized)
    # pvt = readData("pvt", uncategorized)

    # print(len(data), len(third), len(pvt))
    # webStats = {}
    # provider_count = {}
    # provider_risk = {}
    # provider_websites ={}
    # provider_websites_conc = {}
    # totalwebsites, totalCount = findTotal(data)

    # for r in range(4):
    #     rank = 100*(10**r)
    #     webStats[rank] = {}
    #     webStats[rank]["third"] = findThird(third, rank)
    #     webStats[rank]["redundant"], webStats[rank]["exclusive"] = findExclusiveThird(third, data, rank, groupMAP)
    #     webStats[rank]["redAll"], webStats[rank]["excAll"] = findExclusiveThird(data, data, rank, groupMAP)

    #     webStats[rank]["third-pvt"] = findPvtThird(webStats[rank]["redundant"],third, pvt)
    #     webStats[rank]["third-third"] = findThirdThird(webStats[rank]["redundant"], third, pvt)

    #     # provider_websites_conc[rank], provider_count[rank] = majorProviders(third, rank, groupMAP)
    #     # provider_websites_conc[rank], provider_count[rank] = majorProviders(data, rank, groupMAP)

    #     # provider_websites[rank], provider_risk[rank] = majorRiskyProviders(third,rank, groupMAP,webStats[rank]["redundant"])
    #     provider_websites[rank], provider_risk[rank] = majorRiskyProviders(data,rank, groupMAP,webStats[rank]["redAll"])


    #     # top10 = dict(itertools.islice(provider_count[rank].items(), 10))
    #     # top10risk = dict(itertools.islice(provider_risk[rank].items(),10))
    #     # print(len(top10))

    #     # for i, j in top10.items():
    #     #     try:
    #     #         grp = groupIDs[i]
    #     #         print(i, grp, j)
    #     #     except:
    #     #         print(i,j)

    #     # plotTopConcentration(top10, rank, totalCount,"conc")
    #     # plotTopConcentration(top10risk, rank, totalCount,"risk")
    #     # top5 = dict(itertools.islice(provider_count[rank].items(), 5))
    #     # plotTopConcRisk(top5, provider_risk[rank], rank, totalCount,"conc-risk")

        
        
    
    
    # # plotWebsiteStats(webStats,totalCount)

    # for provider, websites in provider_websites[100000].items():
    #     websites = [str(r) + "-" + w for r,w in websites]
    #     websites = ":".join(websites)
    #     print(f"{provider},{websites}")








if __name__ == "__main__":
    main()