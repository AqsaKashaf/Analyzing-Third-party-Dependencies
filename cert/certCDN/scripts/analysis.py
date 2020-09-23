







import sys, tldextract


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
        ca_url = l[0]
        ca = ca_url_map[ca_url]
        nsDomain = l[1]
        if("awsdns-" in nsDomain):
            ns = "aws"
        else:
            ns = ns_domain_map[nsDomain]
        if(ns not in ns_ca):
            ns_ca[ns] = set()
        ns_ca[ns].add(ca)
        if(ca not in ca_ns):
            ca_ns[ca] = set()
        ca_ns[ca].add(ca)
    
    f.close()

    # print(cdn_ns)
    return ns_ca,ca_ns

def readData(filename, ca_url_map):
    f = open(filename,"r")
    data = {}
    for l in f:
        l = l.strip().split(",")
        ca_url = l[0].lower()
        ca = ca_url_map[ca_url]
        cdn = l[1].lower()
        if(ca not in data):
            data[ca] = set()
        if(cdn != "none"):
            data[ca].add(cdn)
    
    return data

def findExclusiveThird(data):
    exclusive = set()
    redundant = set()
    for ca, providers in data.items():
        if(len(data[ca]) == 1):
            exclusive.add(ca)
        elif(len(data[ca]) > 1):
            redundant.add(ca)
        
    return redundant,exclusive

def readcaUrldata(filename, ca_url_map):
    data = {}
    cas = set()
    f = open(filename,"r")
    for line in f:
        line = line.strip().split(",")
        r = int(line[0])
        w = line[1]
        key = r,w
        if(key not in data):
            data[key] = set()
        
        ca_url = line[2].lower()
        if(ca_url != "none"):
            ca_url = tldextract.extract(ca_url)
            ca_url = ca_url.domain + "." + ca_url.suffix
            ca = ca_url_map[ca_url]
            cas.add(ca)
            data[key].add(ca)
            
    
    return data,cas
    
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

def find_enhanced_third(pvt_web_ca, stapled, third_ca_ns):

    websites = set()
    websitesRank = {}
    websitesRank[1000] = 0
    websitesRank[10000] = 0
    websitesRank[100000] = 0
    websitesRank[100] = 0
    for (r,w),ca in pvt_web_ca.items():
        if("digicert" not in ca and "globalsign" not in ca and "entrustinc" not in ca):
            if(ca in third_ca_ns and len(third_ca_ns[ca]) > 0 and (r,w) not in stapled):
                websites.add((r,w))
                if(r <= 100000):
                    websitesRank[100000]+=1 #//.add((r,w))
                    # print(r,w,ca, third_ca_ns[ca])
                if(r <= 10000):
                    websitesRank[10000]+=1 #.add((r,w))
                    print(r,w,ca)
                if(r <= 1000):
                    websitesRank[1000]+=1 #.add((r,w))
                    
                if(r <= 100):
                    websitesRank[100]+=1 #.add((r,w))
                    # print(r,w)
    return websites, websitesRank




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



def readCAdata(web_ca_pvt,caData):

    f = open(web_ca_pvt,"r")
    data = {}
    for ln in f:
        ln = ln.strip().split(",")
        r = int(ln[0])
        w = ln[1]
        ca = list(caData[(r,w)])[0]
        data[(r,w)] = ca

    return data

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



def main():

    filename = sys.argv[1]
    ca_url_map = readCAMap("../url-ca-map")
    caData, _ = readcaUrldata("../CA_URL_CURRENT", ca_url_map)
    
    data = readData(filename, ca_url_map)
    
    for ca,cdn in data.items():
        for c in cdn:
            print(f"{ca},{c}")

    # stapleData = readStapleData("../stapleCurrent")
    # redundant,exclusive = findExclusiveThird(data)

    # print(len(data),len(redundant), len(exclusive), len(caData))
    # # print(redundant)


    # pvt_web_ca = readCAdata("../pvt",caData)


    # websites, websites_rannk = find_enhanced_third(pvt_web_ca, stapleData,data)
    # print(len(websites), websites_rannk)



    # damage, damage_count = readDamage("../data/CAdamage3rd",100000)

    # damageall, damage_countall = readDamage("../data/CAdamageAll",100000)

    # findFailedRedundancy(damage, third_ns_cdn)

    # total = 0
    # for i, j in data.items():
    #     if(i in exclusive):
    #         # for cdn in j:
    #         try:
    #             print(i, j, damage_count[i])
    #             total += damage_count[i]
    #         except KeyError:
    #             # print("keyerror",i)
    #             print(i, j, damage_countall[i])
    #             total += damage_countall[i]
    
    # print(total)





if __name__ == "__main__":
    main()
