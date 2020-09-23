
import sys
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import numpy as np
import itertools,math

CA_CDN_FILEPATH = "../cert/certCDN/cert-cdn"
CA_CONC_FILEPATH = "../cert/data/CAconcAll"
CA_DAMAGE_FILEPATH = "../cert/data/CAdamageAll"
CDN_DATA_FILE = "./CDNCurrent"

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (13,9)
plt.rcParams["axes.labelsize"] = 40
plt.rcParams["axes.titlesize"] =  30
plt.rcParams["lines.linewidth"] = 3
plt.rcParams["xtick.labelsize"] = 40
plt.rcParams["ytick.labelsize"] = 40
plt.rcParams["legend.fontsize"] = 40




def autolabel(rects,ax):
    for rect in rects:
        h = rect.get_height()
        ax.annotate(int(math.ceil(h)),
                    xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext = (0,3),
                    textcoords="offset points",
                    ha="center", va="bottom", size=28)


def plotTopTotal(topk,riskValues, rank, total, prefix):

    labels = [e.capitalize() for e in topk.keys()]

    x = np.arange(len(labels))
    width = 0.35

    fig,ax = plt.subplots()

    concentration = []
    risk = []
    for k,count in topk.items():
       
        # concentration.append(count/total[rank])
        concentration.append(count/rank*100)
        # risk.append(riskValues[k]/total[rank])
        risk.append(riskValues[k]/rank*100)

    patterns = [ "|||" , "\\" , "/" , "+" , "-", "..", "**","x", "oo", "O" ]
    # r = []
    # for p,c in concentration.items():
    r=ax.bar(x-width/2, concentration, width,label=r"$Web \to CDN \cup Web \to CA \to CDN$ ",hatch=patterns[0],color='white', edgecolor='black')
    rEx = ax.bar(x+width/2,risk,width,label=r"$Web \to CDN$ ",hatch=patterns[1],color='white', edgecolor='black')

    ax.set_ylabel("Percentage  of Websites")

    ax.set_xlabel("CDN Providers")

    ax.set_xticks(x)

    ax.set_xticklabels(labels,rotation=40,ha="right")
    lgd = ax.legend(bbox_to_anchor=(0.5,1.35),loc="upper center",ncol=1)
    # for rect in r:
    autolabel(r,ax)
    autolabel(rEx,ax)
    
    plt.savefig(f"figures/provider_{prefix}_{rank}.pdf",bbox_extra_artists=(lgd,),bbox_inches='tight')
    # , bbox_extra_artists=(lgd,), 
    


def readCA_CDNdep(filename, ca_url_map):

   
    # print(set(ns_domain_map.values()))
    f = open(filename,"r")

    cdn_ca = {}
    ca_cdn = {}
    for l in f:
        l = l.strip().split(",")
        ca_url = l[0].lower()
        ca = ca_url_map[ca_url]
        cdn = l[1].lower()
        if(cdn not in cdn_ca):
            cdn_ca[cdn] = set()
        cdn_ca[cdn].add(ca)
        if(ca not in ca_cdn):
            ca_cdn[ca] = set()
        ca_cdn[ca].add(ca)
    
    f.close()

    # print(cdn_ns)
    return cdn_ca,ca_cdn


def readCAMap(filename):
    f = open(filename,"r")
    urlca = {}
    for line in f:
        # print(line)
        line= line.strip().split(" ")
        url = line[0].lower()
        ca = line[1].lower()
        urlca[url] = ca
    
    return urlca

def caConcentrationAnalysis(damageDir3rdNS,rank):

    # print(ns_domain_map)
    ca_url_map = readCAMap("../cert/url-ca-map")
    
    third_cdn_ca,third_ca_cdn = readCA_CDNdep(CA_CDN_FILEPATH, ca_url_map)
    # print(third_ns_ca)
    CA_CONC_ALL,_ = readDamage(CA_CONC_FILEPATH,rank)

    CDN_CONC_CA = {}
    for cdn, damage in damageDir3rdNS.items():
        damage_dir_3rd = damageDir3rdNS[cdn]
        ca_deps_damage = set()
        try:
            ca_deps = third_cdn_ca[cdn]
            for ca in ca_deps:
                ca_deps_damage = ca_deps_damage.union(CA_CONC_ALL[ca])
        except KeyError:
            print(cdn)
            pass

        CDN_CONC_CA[cdn] = damage_dir_3rd.union(ca_deps_damage)
    
    CDN_CONC_CA_COUNT = {}
    for pid, websites in CDN_CONC_CA.items():
        CDN_CONC_CA_COUNT[pid] = len(websites)

    CDN_CONC_CA_COUNT = {k: v for k, v in sorted(CDN_CONC_CA_COUNT.items(), key=lambda item: item[1], reverse=True)}

    return CDN_CONC_CA, CDN_CONC_CA_COUNT

def caRiskAnalysis(damageDir3rdNS,rank):


    ca_url_map = readCAMap("../cert/url-ca-map")
    
    third_cdn_ca,third_ca_cdn = readCA_CDNdep(CA_CDN_FILEPATH, ca_url_map)

    exclusiveDep = findExclusive(third_ca_cdn)
    # print(third_ns_ca)
    CA_DAMAGE_ALL,_ = readDamage(CA_DAMAGE_FILEPATH,rank)

    CDN_RISK_CA = {}
    for cdn, damage in damageDir3rdNS.items():
        damage_dir_3rd = damageDir3rdNS[cdn]
        ca_deps_damage = set()
        try:
            ca_deps = third_cdn_ca[cdn]
            for ca in ca_deps:
                if(ca in exclusiveDep):
                    ca_deps_damage = ca_deps_damage.union(CA_DAMAGE_ALL[ca])
        except KeyError:
            # print(ns)
            pass

        CDN_RISK_CA[cdn] = damage_dir_3rd.union(ca_deps_damage)
    
    CDN_RISK_CA_COUNT = {}
    for pid, websites in CDN_RISK_CA.items():
        CDN_RISK_CA_COUNT[pid] = len(websites)

    CDN_RISK_CA_COUNT = {k: v for k, v in sorted(CDN_RISK_CA_COUNT.items(), key=lambda item: item[1], reverse=True)}

    return CDN_RISK_CA, CDN_RISK_CA_COUNT


def findExclusive(data):

    exclusive = set()
    for i,j in data.items():
        if(len(j) == 1):
            exclusive.add(i)

    return exclusive



def readDamage(filename,rank):

    ns_damage_dir_3rd = {}
    f = open(filename,"r")
    for l in f:
        l = l.strip().split(",")
        ns=l[0].lower()
        websites = l[1].split(":")
        ns_damage_dir_3rd[ns] = set()
        
        for w in websites:
            if(w!=""):
                w = w.split("-")
                r = int(w[0])
                w = w[1]
                if(r <= rank):
                    ns_damage_dir_3rd[ns].add((r,w))
    
    f.close()

    damage_count = {}
    for pid, websites in ns_damage_dir_3rd.items():
        damage_count[pid] = len(websites)

    damage_count = {k: v for k, v in sorted(damage_count.items(), key=lambda item: item[1], reverse=True)}
    return ns_damage_dir_3rd,damage_count

def readData(filename):

    data = {}
    f = open(filename,"r")
    for line in f:
        line = line.strip().split(",")
        rank = int(line[0])
        if(rank <= 100000):
            website = line[1]
            provider = line[2]
            key = rank,website
            if(key not in data):
                data[key] = set()
            if(provider != "none"):
                data[key].add(provider)
    
    return data

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






def main():

    concFile = sys.argv[1] 
    riskFile = sys.argv[2]

    data = readData(CDN_DATA_FILE)
    totalwebsites, totalCount = findTotal(data)
    

    for r in range(4):
        rank = 100*(10**r)
        # #3concentration analysis ude to cdn-ns dep
        concDir,countDir = readDamage(concFile,rank)

        concentration_ca,count_ca = caConcentrationAnalysis(concDir, rank)
        top5 = dict(itertools.islice(count_ca.items(), 5))
        plotTopTotal(top5, countDir, rank, totalCount,"conc-ca-cdn")

        # # #risk analysis due to cdn-ns dep
        

        damageDir, countDir = readDamage(riskFile,rank)
        

        risk, riskCount = caRiskAnalysis(damageDir,rank)
        top5risk = dict(itertools.islice(riskCount.items(), 5))
        plotTopTotal(top5risk, countDir, rank, totalCount,"risk-ca-cdn")


    # for provider, websites in risk.items():
    #     websites = [str(r) + "-" + w for r,w in websites]
    #     websites = ":".join(websites)
    #     print(f"{provider},{websites}")


if __name__ == "__main__":
    main()