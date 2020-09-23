


import sys,json, tldextract
import os.path


def attachRank():
    f = open("../list1m2020.csv","r")
    rank = 1
    data = {}
    for line in f:
        line = line.strip()        
        data[line] = rank
        rank += 1
    
    return data

def readCname(filename,details):
    f = open(filename,"r")
    data = json.load(f)
    
    for i,j in data.items():
        website = i
        
        if(i != "dummy" and type(data[i]) is dict and "everything" in data[i]):
            if(website not in details):
                details[website] = {}
            
            assets = data[i]["everything"]
            for item in assets:
                hostname = item["hostname"]
                cnames = item["cnames"]
                cdn = item["cdn"] if item["cdn"] else "none"
                headerguess = item["headerguess"]
                # if(headerguess):
                #     cdn = "none"
                cnameChain = ""
                for cname in cnames:
                    tld_cdn = tldextract.extract(cname)
                    tld_cdn = tld_cdn.domain + "." + tld_cdn.suffix
                    cnameChain += tld_cdn + "->"
                cnameChain = cnameChain.rstrip("->")
                tld_host = tldextract.extract(hostname)
                tld_host = tld_host.domain + "." + tld_host.suffix
                tld_cdn = cnameChain +":" + cdn
                if(tld_host not in details[website]):
                    details[website][tld_host] = set()
                details[website][tld_host].add(tld_cdn)
                

    return details


def readCDN(filename,cdns,error):
    f = open(filename,"r")
    data = json.load(f)
    cdn = None
    
    for i,j in data.items():
        website = i
        # print(i)
        
        if(website not in cdns):
            cdns[website] = set()
        if(type(data[i]) is dict):
            if("basecdn" in data[i] and data[i]["basecdn"]):
                cdn = data[i]["basecdn"]
                # print(website,cdn)
                cdns[website].add(cdn)
            
            if("assetcdn" in data[i] and data[i]["assetcdn"]):
                cdn = data[i]["assetcdn"]
                cdns[website].add(cdn)
            
        else:
            error.add(i)
            

        
    return cdns, error

def validateJson(filename):
    f = open(filename,"r")
    data = json.load(f)

def generateJson(filename):
    f = open(filename,"r")
    started = False
    cnames = {}
    website = ""
    curCname = ""
    fw = open(filename + "json","w")
    # print("{")
    fw.write("{\n")
    
    for line in f:    

        if("signal:" in line or "Phantomjs had an error" in line or "invalid character" in line or "floating point exception" in line):
            continue

        elif(not started):
            if("Oops error for website" in line):
                website = line.strip().split(",")[0]
                line = '"' + website + '":' 
                line += '"error",\n'
            else:
                website = line.strip().split(",")[0]
                line = '"' + website + '":\n' 
                started = True



        if(line.startswith(" }")):
            started = False
            line = line + ",\n"
        
        # print (line.strip("\n"))
        fw.write(line)
    
    # print('"dummy": {}\n}')
    fw.write('"dummy": {}\n}')
    fw.close()

def printCDNs(data):

    ranks = attachRank()
    for w, cdns in data.items():
        
        if(w != "dummy"):
            r = ranks[w]
            if(len(cdns) == 0):
                print(f"{r},{w},none")
            else:
                for c in cdns:
                    print(f"{r},{w},{c}")

def main():

    filename = sys.argv[1]
    
    # for i in range(40):
        
    #     if os.path.isfile(filename + str(i)):
    #         print (i)
    #         generateJson(filename + str(i))
    #         validateJson(filename + str(i) + "json")

    data = {}
    error = set()
    for i in range(40):
        if os.path.isfile(filename+str(i)+"json"):
            # print (i)
            data, error = readCDN(filename+str(i)+"json", data, error)
            # data = readCname(filename+str(i)+"json", data)


    # # print(len(error))
    ranks = attachRank()

    printCDNs(data)
    # for e in error:
    #     print(e)
    # hosts = set()
    # for w,details in data.items():
    #     if(w != "dummy"):
    #         rank = ranks[w]

    #         if(len(details) == 0):
    #             cdn = "none"
    #             print(f"{rank},{w},{cdn}")
    #         else:
    #             for h,cnames in details.items():
    #                 # hosts.add(h)
    #                 print(f"{rank},{w},{h},{cnames}")
    
    # print(len(data.keys()))
    # for h in hosts:
    #     print(h)
    # validateJson(sys.argv[1])

if __name__ == "__main__":
    main()