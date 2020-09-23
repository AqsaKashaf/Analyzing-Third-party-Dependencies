
import sys, tldextract

def applySOA(data, cdnMap):
    
    f = open("../soaCDN/cname-soa-cont","r")
    hostData = {}
    for line in f:
        line = line.strip().split(",")
        host = line[0]
        if host not in hostData:
            hostData[host] = {}
            hostData[host]["soa"] = ""
            hostData[host]["contact"] = ""
        if(line[1] != "NXDOMAIN" and line[1] != ""):
            hostData[host]["soa"] = line[1].strip(".")
            # if(host == "phncdn.com"):
            #     print(host,hostData[host]["soa"])
        if(line[2] != "NXDOMAIN" and line[2] != ""):
            hostData[host]["contact"] = line[2]

    f.close()

    nsData = {}
    f = open("../../dns/soaNS/ns-soa-cont-20","r")
    for line in f:
        line = line.strip().split(",")
        ns = line[0]
        if ns not in nsData:
            nsData[ns] = {}
            nsData[ns]["soa"] = ""
            nsData[ns]["contact"] = ""
        if(line[1] != "NXDOMAIN" and line[1] != ""):
            nsData[ns]["soa"] = line[1].strip(".")
            # if(website == "pornhub.com"):
            #     print(website, webData[website]["soa"])
        if(line[2] != "NXDOMAIN" and line[2] != ""):
            nsData[ns]["contact"] = line[2]
        
    
    f.close()
    pvt = set()
    third = set()
    thirdcdns = set()
    for (cdn),nameservers in data.items():
        cdn = cdn.lower()
        for ns in nameservers:
            if("awsdns-" in ns or "dnsmadeeasy" in ns):
                third.add((cdn,ns))
                thirdcdns.add(cdn)
            elif("akam" in ns and cdn == "akamai"):
                pvt.add((cdn,ns))
            else:
                if(ns in nsData):
                    nsSOA = nsData[ns]["soa"]
                    flag = False
                    try:
                        cnames = cdnMap[cdn]
                        for cname in cnames:
                            if(cname in hostData):
                                cnameSOA = hostData[cname]["soa"]
                                if(nsSOA == cnameSOA):
                                    flag = True
                                    break

                        if(not flag):
                            third.add((cdn,ns))
                            thirdcdns.add(cdn)
                        else:
                            pvt.add((cdn,ns))
                    except KeyError:
                        # print(cdnMap)
                        print("keyerror",cdn,ns)
                else:
                    # print(cdn,ns)
                    pvt.add((cdn,ns))    
                
    # print(len(third), len(pvt))
    # print(len(thirdcdns))
    # print(thirdcdns)
    return third,pvt


def readData(filename, cdns):
    f = open(filename,"r")
    data = {}
    for ln in f:
        ln = ln.strip().split(",")
        cdn = (ln[0].split(" ")[0]).lower()
        if(cdn in cdns):
            if(cdn not in data):
                data[cdn] = set()
            data[cdn].add(ln[1])

    return data

def readCDNMap():

    f = open("../cdnMap","r")
    cnameMap = {}
    cdnMap = {}
    for line in f:
        line = line.strip().split(",")
        cdn = line[0].lower()
        if(cdn not in cdnMap):
            cdnMap[cdn] = set()
        cnames = line[1].split(" ")
        for c in cnames:
            cnameMap[c.lower()] = cdn
            cdnMap[cdn].add(c)

    return cnameMap, cdnMap

def readcdndata(filename):

    cdns = set()
    f = open(filename,"r")
    for line in f:
        line = line.strip().split(",")
        cdn = line[2].lower()
        if(cdn!="none"):
            cdns.add(cdn)
    
    return cdns

def groupBySOA(data, cdnData, pvt):

    nsData = {}
    f = open("../../dns/soaNS/ns-soa-cont-20","r")
    for line in f:
        line = line.strip().split(",")
        ns = line[0]
        if ns not in nsData:
            nsData[ns] = {}
            nsData[ns]["soa"] = ""
            nsData[ns]["contact"] = ""
        if(line[1] != "NXDOMAIN" and line[1] != ""):
            nsData[ns]["soa"] = line[1].strip(".")
            # if(website == "pornhub.com"):
            #     print(website, webData[website]["soa"])
        if(line[2] != "NXDOMAIN" and line[2] != ""):
            nsData[ns]["contact"] = line[2]
    
    f.close()

    groups = {}
    for cdn,ns in data.items():
        cdn = cdn.lower()
        if cdn in cdnData:
            for n in ns:
                if (cdn,n) not in pvt:
                    if(n in nsData):
                        soa = nsData[n]["soa"]
                        soa = tldextract.extract(soa).domain
                        if("awsdns" in n):
                            soa = "awsdns"
                        
                        if(soa not in groups):
                            groups[soa] = set()
                        
                        groups[soa].add(n)
                    
                    else:
                        if(n not in groups):
                            groups[n] = set()
                    
                        groups[n].add(n)
                else:
                    if(n not in groups):
                        groups[n] = set()
                
                    groups[n].add(n)
    
    groupmap = {}
    for i,j in groups.items():
        # print (j)
        for entries in j:
            groupmap[entries] = i

    return groups, groupmap
            
def findThird(third):
    return third

def findRedundant(data,third, groups):
    redundant = set()
    exclusive = set()
    for cdn,ns in third:
        ns = data[cdn]
        if(len(ns) > 1):
            grpIds = set()
            for n in ns:
                grpIds.add(groups[n])
            if(len(grpIds)>1):
                redundant.add(cdn)
            else:
                exclusive.add(cdn)
        else:
            exclusive.add(cdn)
    return redundant, exclusive

def readDataCDN(filename):

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

def findExclusiveThird(third, data, rank):
    exclusive = set()
    redundant = set()
    for (r,w), providers in third.items():
        if(r <= rank):
            if(len(data[(r,w)]) == 1):
                exclusive.add((r,w))
            else:
                redundant.add((r,w))
        
    return redundant,exclusive

def main():
    filename = sys.argv[1]
    cdnData = readcdndata("../CDNCurrent")
    data = readData(filename, cdnData)

    
    print(len(cdnData), len(data))
    for c in cdnData:
        if c not in data:
            print(c)
    # cnameMap, cdnMap = readCDNMap()
    # print (cdnMap)
    # third, pvt = applySOA(data, cdnMap)
    # print(len(third))

    # # # 
    # groups, grp_map = groupBySOA(data, cdnData, pvt)
    

    # # findThird(third)
    # redundant, exclusive = findRedundant(data,third, grp_map)
    # print("exclusive",exclusive)




    # for all exclusive cdn -> ns links 
        # cdn-damage = web -> cdn exc links done
        # ns-damage = web -> ns ex links union cdn-damage


    # for i, grps in groups.items():
    #     grps = " ".join(grps)
    #     print(f"{i},{grps}")

    # for cdn,ns in third:
    #     print(f"{cdn},{ns}")






if __name__ == "__main__":
    main()