
import sys
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import numpy as np
import itertools, math

CDN_NS_FILEPATH = "../cdn/cdnNS/cdn-ns"
CDN_NS_THIRD_FILEPATH = "../cdn/cdnNS/third-cdn-ns"
CA_NS_FILEPATH = "../cert/certNS/CA_NS"
CA_NS_THIRD_FILEPATH = "../cert/certNS/third-cert-ns"
CDN_NS_GROUPS_FILE = "../cdn/cdnNS/groups-cdn-ns"
CA_NS_GROUPS_FILE = "../cert/certNS/groups-cert-ns"
# CDN_CONC_FILEPATH = "../cdn/data/CDNconcTotalAll"
CDN_CONC_FILEPATH = "../cdn/data/CDNconcAll"

CA_CONC_FILEPATH = "../cert/data/CAconcAll"
# CDN_DAMAGE_FILEPATH = "../cdn/data/CDNdamageTotalAll"
CDN_DAMAGE_FILEPATH = "../cdn/data/CDNdamageAll"

CA_DAMAGE_FILEPATH = "../cert/data/CAdamageAll"
DNS_DATA_FILE = "./DNSCurrentv1"

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
    patterns = [ "|||" , "\\" , "/" , "+" , "-", "..", "**","x", "oo", "O" ]
    concentration = []
    risk = []
    for k,count in topk.items():
       
        concentration.append(count/rank*100)
        risk.append(riskValues[k]/rank*100)

    
    # r = []
    # for p,c in concentration.items():
    r=ax.bar(x-width/2, concentration, width,hatch=patterns[0],color='white', edgecolor='black',label=r"$Web \to DNS \cup Web \to CA \to DNS$") #\cup Web \to CA \to CDN \to DNS$ ")
    rEx = ax.bar(x+width/2,risk,width,label=r"$Web \to DNS$", hatch=patterns[1],color='white', edgecolor='black')

    ax.set_ylabel("Percentage  of Websites")

    ax.set_xlabel("DNS Providers")

    ax.set_xticks(x)

    ax.set_xticklabels(labels,rotation=40) #,ha="right")
    lgd = ax.legend(bbox_to_anchor=(0.5,1.35),loc="upper center",ncol=1)
    # for rect in r:
    autolabel(r,ax)
    autolabel(rEx,ax)
    
    plt.savefig(f"figures/provider_{prefix}_{rank}_DNS.pdf",bbox_extra_artists=(lgd,),bbox_inches='tight')
    # , bbox_extra_artists=(lgd,), 
    
def readCDN_NSdep():

    f = open(CDN_NS_GROUPS_FILE,"r")

    ns_domain_map = {}
    for ln in f:
        ln = ln.strip().split(",")
        ns = ln[0].lower()
        ns = ns.split(".")[0]
        nsdomains = ln[1].split(" ")
        for d in nsdomains:
            ns_domain_map[d] = ns
    
    f.close()
    # print(set(ns_domain_map.values()))
    f = open(CDN_NS_FILEPATH,"r")

    cdn_ns = {}
    for l in f:
        l = l.strip().split(",")
        cdn = l[0].split(" ")[0].lower()
        nsDomain = l[1]
        try:
            ns = ns_domain_map[nsDomain]
        except KeyError:
            ns = nsDomain
        if(cdn not in cdn_ns):
            cdn_ns[cdn] = set()
        cdn_ns[cdn].add(cdn)
    
    f.close()

    f = open(CDN_NS_THIRD_FILEPATH,"r")

    ns_cdn = {}
    for l in f:
        l = l.strip().split(",")
        cdn = l[0]
        nsDomain = l[1]
        ns = ns_domain_map[nsDomain]
        if(ns not in ns_cdn):
            ns_cdn[ns] = set()
        ns_cdn[ns].add(cdn)
    
    f.close()

    # print(cdn_ns)
    return ns_cdn,cdn_ns




def cdnConcentrationAnalysis(damageDir3rdNS,rank):


    CDN_NS,_ = readCDN_NSdep()
    CDN_CONC_ALL,_ = readDamage(CDN_CONC_FILEPATH,rank)

    DNS_CONC_CDN = {}
    for ns, damage in damageDir3rdNS.items():
        damage_dir_3rd = damageDir3rdNS[ns]
        cdn_deps_damage = set()
        try:
            cdn_deps = CDN_NS[ns]
            for cdn in cdn_deps:
                cdn_deps_damage = cdn_deps_damage.union(CDN_CONC_ALL[cdn])
        except KeyError:
            # print(ns)
            pass

        DNS_CONC_CDN[ns] = damage_dir_3rd.union(cdn_deps_damage)
    
    DNS_CONC_CDN_COUNT = {}
    for pid, websites in DNS_CONC_CDN.items():
        DNS_CONC_CDN_COUNT[pid] = len(websites)

    DNS_CONC_CDN_COUNT = {k: v for k, v in sorted(DNS_CONC_CDN_COUNT.items(), key=lambda item: item[1], reverse=True)}

    return DNS_CONC_CDN, DNS_CONC_CDN_COUNT


def readGroups():
    f = open(CA_NS_GROUPS_FILE,"r")

    ns_domain_map = {}
    for ln in f:
        ln = ln.strip().split(",")
        ns = ln[0].lower()
        ns = ns.split(".")[0]
        nsdomains = ln[1].split(" ")
        for d in nsdomains:
            ns_domain_map[d] = ns
    
    f.close()
    return ns_domain_map

def readCA_NSdep(filename,ns_domain_map, ca_url_map):

   
    # print(set(ns_domain_map.values()))
    f = open(filename,"r")

    ns_ca = {}
    ca_ns = {}
    for l in f:
        l = l.strip().split(",")
        ca_url = l[0].lower()
        ca = ca_url_map[ca_url]
        nsDomain = l[1]
        if("awsdns-" in nsDomain):
            ns = "aws"
        else:
            ns = ns_domain_map[nsDomain]
        if(ca not in ca_ns):
            ca_ns[ca] = set()
        ca_ns[ca].add(ca)
    
    f.close()

    f = open(CA_NS_THIRD_FILEPATH,"r")

    for l in f:
        l = l.strip().split(",")
        ca_url = l[0].lower()
        ca = ca_url_map[ca_url]
        nsDomain = l[1]
        if("awsdns-" in nsDomain):
            ns = "aws"
        else:
            ns = ns_domain_map[nsDomain]
        if(ns not in ns_ca):
            ns_ca[ns] = set()
        ns_ca[ns].add(ca)
    
    f.close()


    # print(cdn_ns)
    return ns_ca,ca_ns


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


    ns_domain_map = readGroups()
    # print(ns_domain_map)
    ca_url_map = readCAMap("../cert/url-ca-map")
    
    third_ns_ca,third_ca_ns = readCA_NSdep(CA_NS_FILEPATH, ns_domain_map, ca_url_map)
    print(third_ns_ca["dnsmadeeasy"])
    
    CA_CONC_ALL,_ = readDamage(CA_CONC_FILEPATH,rank)

    DNS_CONC_CA = {}
    for ns, damage in damageDir3rdNS.items():
        damage_dir_3rd = damageDir3rdNS[ns]
        ca_deps_damage = set()
        try:
            ca_deps = third_ns_ca[ns]
            for ca in ca_deps:
                ca_deps_damage = ca_deps_damage.union(CA_CONC_ALL[ca])
                if(ns == "dnsmadeeasy"):
                    print(len(CA_CONC_ALL[ca]))
        except KeyError:
            if(ns == "dnsmadeeasy"):
              print(ns)
            pass

        DNS_CONC_CA[ns] = damage_dir_3rd.union(ca_deps_damage)
        if(ns == "dnsmadeeasy"):
            print(ns, len(damage_dir_3rd), len(ca_deps_damage), len(DNS_CONC_CA[ns]))
    
    DNS_CONC_CA_COUNT = {}
    for pid, websites in DNS_CONC_CA.items():
        DNS_CONC_CA_COUNT[pid] = len(websites)

    DNS_CONC_CA_COUNT = {k: v for k, v in sorted(DNS_CONC_CA_COUNT.items(), key=lambda item: item[1], reverse=True)}

    return DNS_CONC_CA, DNS_CONC_CA_COUNT

def caRiskAnalysis(damageDir3rdNS,rank):


    ns_domain_map = readGroups()
    # print(ns_domain_map)
    ca_url_map = readCAMap("../cert/url-ca-map")
    


    third_ns_ca,third_ca_ns = readCA_NSdep(CA_NS_FILEPATH, ns_domain_map, ca_url_map)

    exclusiveDep = findExclusive(third_ca_ns)
    # print(third_ns_ca)
    CA_DAMAGE_ALL,_ = readDamage(CA_DAMAGE_FILEPATH,rank)

    DNS_RISK_CA = {}
    for ns, damage in damageDir3rdNS.items():
        damage_dir_3rd = damageDir3rdNS[ns]
        ca_deps_damage = set()
        try:
            ca_deps = third_ns_ca[ns]
            for ca in ca_deps:
                if(ca in exclusiveDep):
                    ca_deps_damage = ca_deps_damage.union(CA_DAMAGE_ALL[ca])
        except KeyError:
            # print(ns)
            pass

        DNS_RISK_CA[ns] = damage_dir_3rd.union(ca_deps_damage)
    
    DNS_RISK_CA_COUNT = {}
    for pid, websites in DNS_RISK_CA.items():
        DNS_RISK_CA_COUNT[pid] = len(websites)

    DNS_RISK_CA_COUNT = {k: v for k, v in sorted(DNS_RISK_CA_COUNT.items(), key=lambda item: item[1], reverse=True)}

    return DNS_RISK_CA, DNS_RISK_CA_COUNT


def findExclusive(data):

    exclusive = set()
    for i,j in data.items():
        if(len(j) == 1):
            exclusive.add(i)

    return exclusive

def cdnRiskAnalysis(damageDir3rdNS,rank):


    NS_CDN,CDN_NS = readCDN_NSdep()
    # print (NS_CDN.keys())
    exclusiveDep = findExclusive(CDN_NS)
    print(exclusiveDep)
    cdn_damage,_ = readDamage(CDN_DAMAGE_FILEPATH,rank)

    DNS_RISK_CDN = {}
    for ns, damage in damageDir3rdNS.items():
        damage_dir_3rd = damageDir3rdNS[ns]
        cdn_deps_damage = set()
        try:
            cdn_deps = NS_CDN[ns]
            
            for cdn in cdn_deps:
                # print(cdn, ns)
                if(cdn in exclusiveDep):
                    if("aws" in ns):
                        print(cdn, ns, cdn_damage[cdn])
                    cdn_deps_damage = cdn_deps_damage.union(cdn_damage[cdn])

        except KeyError:
            # print(ns)
            pass

        DNS_RISK_CDN[ns] = damage_dir_3rd.union(cdn_deps_damage)
    
    DNS_RISK_CDN_COUNT = {}
    for pid, websites in DNS_RISK_CDN.items():
        DNS_RISK_CDN_COUNT[pid] = len(websites)

    DNS_RISK_CDN_COUNT = {k: v for k, v in sorted(DNS_RISK_CDN_COUNT.items(), key=lambda item: item[1], reverse=True)}

    return DNS_RISK_CDN, DNS_RISK_CDN_COUNT


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



def readUncategorized():
    uncat = set()
    f = open("uncategorized", "r")
    for line in f:
        line = line.strip()
        uncat.add(line.lower())

    f.close()
    return uncat

def combineAll(dict1, dict2):

    dict3 = {}
    for i,j in dict1.items():
        dict3[i] = j.union(dict2[i])
    

    count = {}
    for i, j in dict3.items():
        count[i] = len(j)

    count = {k: v for k, v in sorted(count.items(), key=lambda item: item[1], reverse=True)}
    return dict3, count

def main():

    concFile = sys.argv[1] 
    riskFile = sys.argv[2]
    uncategorized = readUncategorized()

    data = readData(DNS_DATA_FILE, uncategorized)
    totalwebsites, totalCount = findTotal(data)

    print(totalCount)
    

    for r in range(4):
        rank = 100*(10**r)
        # #3concentration analysis ude to cdn-ns dep
        concDir,countDir = readDamage(concFile,rank)
        concentration, count = cdnConcentrationAnalysis(concDir,rank)
        top5 = dict(itertools.islice(count.items(), 5))
        plotTopTotal(top5, countDir, rank, totalCount,"conc-cdn-dns")

        # plotTopTotal(top5, countDir, rank, totalCount,"conc-cdn-total-dns")

        # concentration_ca,count_ca = caConcentrationAnalysis(concDir, rank)
        # top5 = dict(itertools.islice(count_ca.items(), 5))
        # plotTopTotal(top5, countDir, rank, totalCount,"conc-ca-dns")

        # total_conc, total_count = combineAll(concentration, concentration_ca)
        # top5 = dict(itertools.islice(total_count.items(), 5))
        # plotTopTotal(top5, countDir, rank, totalCount,"conc-total-dns")


        # #risk analysis due to cdn-ns dep
        damageDir, countDir = readDamage(riskFile,rank)
        

        risk_cdn, riskCount_cdn = cdnRiskAnalysis(damageDir,rank)
        top5risk = dict(itertools.islice(riskCount_cdn.items(), 5))
        plotTopTotal(top5risk, countDir, rank, totalCount,"risk-cdn-dns")

        # plotTopTotal(top5risk, countDir, rank, totalCount,"risk-cdn-total-dns")



        # damageDir, countDir = readDamage(riskFile,rank)
        

        # risk_ca, riskCount_ca = caRiskAnalysis(damageDir,rank)
        # top5risk = dict(itertools.islice(riskCount_ca.items(), 5))
        # plotTopTotal(top5risk, countDir, rank, totalCount,"risk-ca-dns")

        # print(countDir)

        # total_risk, total_risk_count = combineAll(risk_cdn, risk_ca)
        # top5 = dict(itertools.islice(total_risk_count.items(), 5))
        # plotTopTotal(top5, countDir, rank, totalCount,"risk-total-dns")


if __name__ == "__main__":
    main()