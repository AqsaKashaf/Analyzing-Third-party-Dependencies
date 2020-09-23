
import sys, tldextract


def attachRank():
    f = open("../list1m2020.csv","r")
    rank = 1
    data = {}
    for line in f:
        line = line.strip()        
        data[line] = rank
        rank += 1
    
    return data


def main(filename):
    
    # ranks = attachRank()
    f = open(filename, "r")
    data = {}
    for line in f:
        # print(line)
        if("NXDOMAIN" in line or "SERVFAIL" in line):
            line = line.strip().split(",")
            website = line[0]
            data[website] = set()
            data[website].add(("NXDOMAIN","NXDOMAIN"))

        elif("ANSWER: 0" not in line and "+trace" not in line):

            line = line.strip().replace("\t"," ").split("ANSWER SECTION:")



            
            website = line[0].split(";")[0].strip()
            # print(website)
            data[website] = set()
        

           
            if("IN SOA" in line[1]):
                line = line[1].split(" ")
                idx = line.index("SOA")
                ns = line[idx+1]
                ns = tldextract.extract(ns)
                ns = ns.domain + "." + ns.suffix
                contact = line[idx+2]
                data[website].add((ns,contact))
            else:
                pass
                # print(website,"anomaly", line)
            # else:
            #     line = line[1].split(" ")
            #     indices = [i for i, x in enumerate(line) if x == "NS"]
            #     for idx in indices:
            #         ns = line[idx+1]
            #         ns = tldextract.extract(ns)
            #         ns = ns.domain + "." + ns.suffix
            #         data[website].add(ns)
        else:
            line = line.strip().replace("\t"," ").split(" ")
            website = line[0].strip()
            data[website] = set()
            if("SOA" in line):
                idx = line.index("SOA")
                idx = line.index("SOA")
                for i in range(len(line)):
                    if(line[i] == "SOA"):
                        if(line[i+1] != "RRSIG" and line[i-1] == "IN"):
                            idx = i
                            break
                ns = line[idx+1]
                ns = tldextract.extract(ns)
                ns = ns.domain + "." + ns.suffix
                contact = line[idx+2]

                data[website].add((ns,contact))
            else:
                pass
                # print(website,"second anomaly")


    
    for w,nameservers in data.items():
        # rank = ranks[w]
        for n in nameservers:
            soa, contact = n
            print(f"{w},{soa},{contact}")

if __name__ == "__main__":
    filename = sys.argv[1]
    # for i in range(40):
        # print(i)
    main(filename)