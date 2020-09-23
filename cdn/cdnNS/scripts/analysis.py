
import sys

CDN_NS_GROUPS_FILE = "groups-cdn-ns"


def readGroups():
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
    return ns_domain_map



def readCDN_NSdep(filename,ns_domain_map):

   
    # print(set(ns_domain_map.values()))
    f = open(filename,"r")

    ns_cdn = {}
    cdn_ns = {}
    for l in f:
        l = l.strip().split(",")
        cdn = l[0]
        nsDomain = l[1]
        ns = ns_domain_map[nsDomain]
        if(ns not in ns_cdn):
            ns_cdn[ns] = set()
        ns_cdn[ns].add(cdn)
        if(cdn not in cdn_ns):
            cdn_ns[cdn] = set()
        cdn_ns[cdn].add(cdn)
    
    f.close()

    # print(cdn_ns)
    return ns_cdn,cdn_ns

def readData(filename, cdns,ns_domain_map):
    f = open(filename,"r")
    data = {}
    for l in f:
        l = l.strip().split(",")
        cdn = l[0].split(" ")[0].lower()
        if(cdn in cdns):
            nsdomain = l[1]
            ns = ns_domain_map[nsdomain]
            if(cdn not in data):
                data[cdn] = set()
            data[cdn].add(ns)
    
    return data

def findExclusiveThird(third, data):
    exclusive = set()
    redundant = set()
    for cdn, providers in third.items():
        if(len(data[cdn]) == 1):
            exclusive.add(cdn)
        elif(len(data[cdn]) > 1):
            redundant.add(cdn)
        
    return redundant,exclusive

def readcdndata(filename):
    data = {}
    cdns = set()
    f = open(filename,"r")
    for line in f:
        line = line.strip().split(",")
        r = int(line[0])
        w = line[1]
        key = r,w
        if(key not in data):
            data[key] = set()
        
        cdn = line[2].lower()
        if(cdn!="none"):
            cdns.add(cdn)
            data[key].add(cdn)
    
    return data,cdns
    
def readDamage(filename,rank):

    ns_damage_dir_3rd = {}
    f = open(filename,"r")
    for l in f:
        l = l.strip().split(",")
        ns=l[0]
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

def find_enhanced_third(pvt_web_cdn, data, third_cdn_ns):

    websites = set()
    websitesRank = {}
    websitesRank[1000] = 0
    websitesRank[10000] = 0
    websitesRank[100000] = 0
    websitesRank[100] = 0
    for (r,w),cdns in pvt_web_cdn.items():

        for cdn in cdns:
            if(cdn in third_cdn_ns and len(data[(r,w)]) == 1):
                websites.add((r,w))
                if(r <= 100000):
                    websitesRank[100000]+=1 #//.add((r,w))
                    print(r,w)
                if(r <= 10000):
                    websitesRank[10000]+=1 #.add((r,w))
                if(r <= 1000):
                    websitesRank[1000]+=1 #.add((r,w))
                   
                if(r <= 100):
                    websitesRank[100]+=1 #.add((r,w))
                    # print(r,w)
    
    return websites, websitesRank


def findFailedRedundancy(damage, third_ns_cdn):

    websites= {}
    for ns,cdns in third_ns_cdn.items():
        websites[ns] = set()
        flag = True
        if(len(cdns) > 1):
            for c in cdns:
                try:
                    damage_cdn = damage[c]

                    if(flag):
                        websites[ns] = damage_cdn
                        flag = False
                    else:
                        websites[ns] = websites[ns].intersection(damage_cdn)
                except KeyError:
                    print(c)
        print(ns, cdns, len(websites[ns]))

def main():

    filename = sys.argv[1]
    ns_domain_map = readGroups()
    cdnData, uniqueCDNS = readcdndata("../CDNCurrent")
    # print(len(uniqueCDNS))
    data = readData(filename,uniqueCDNS, ns_domain_map)
    all_ns_cdn = {}
    for i,j in data.items():
        for ns in j:
            if(ns not in all_ns_cdn):
                all_ns_cdn[ns] = set()
            all_ns_cdn[ns].add(i)
    # print(len(data))
    
    third_ns_cdn,third_cdn_ns = readCDN_NSdep("third-cdn-ns", ns_domain_map)

    for cdn,ns in third_cdn_ns.items():
        dns = data[cdn]
        for n in dns:
            print(f"{cdn},{n}")


    # print(len(third_cdn_ns))
    # redundant,exclusive = findExclusiveThird(third_cdn_ns, data)

    # print(len(data), len(third_cdn_ns),len(redundant), len(exclusive))
    # print(exclusive)
    # # print(redundant)

    # # for i,j in third_ns_cdn.items():
    # #     print(i,j, len(j))

    # pvt_web_cdn,_= readcdndata("../newPvt")


    # websites, websitesRank = find_enhanced_third(pvt_web_cdn, cdnData,third_cdn_ns)
    # print(len(websites), websitesRank)



    # damage, damage_count = readDamage("../data/CDNdamage3rd",100000)

    # for i,j in third_ns_cdn.items():
    #     for cdn in j:
    #         # if(cdn in exclusive):
    #         try:
    #             print(i,cdn, damage_count[cdn])
    #         except KeyError:
    #             print("keyerror",cdn)

    # # findFailedRedundancy(damage, third_ns_cdn)







if __name__ == "__main__":
    main()