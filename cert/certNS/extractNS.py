
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


def main():
    filename = sys.argv[1]
    ranks = attachRank()
    f = open(filename, "r")
    data = {}
    for line in f:
        if("NXDOMAIN" in line or "SERVFAIL" in line):
            line = line.strip().split(",")
            website = line[0]
            data[website] = "NXDOMAIN"

        elif("ANSWER: 0" not in line):

            line = line.strip().replace("\t"," ").split("ANSWER SECTION:")



            
            website = line[0].split(";")[0].strip()
            # print(website)
            data[website] = set()
        

            if("IN NS" not in line[1]):
                if("IN SOA" in line[1]):
                    line = line[1].split(" ")
                    idx = line.index("SOA")
                    ns = line[idx+1]
                    ns = tldextract.extract(ns)
                    ns = ns.domain + "." + ns.suffix
                    data[website].add(ns)
                else:
                    print(ranks[website],website,"anomaly")
            else:
                line = line[1].split(" ")
                indices = [i for i, x in enumerate(line) if x == "NS"]
                for idx in indices:
                    ns = line[idx+1]
                    ns = tldextract.extract(ns)
                    ns = ns.domain + "." + ns.suffix
                    data[website].add(ns)
        else:
            line = line.strip().replace("\t"," ").split(" ")
            website = line[0].strip()
            data[website] = set()
            if("SOA" in line):
                idx = line.index("SOA")
                ns = line[idx+1]
                ns = tldextract.extract(ns)
                ns = ns.domain + "." + ns.suffix

                data[website].add(ns)
            else:
                print(ranks[website],website,"second anomaly")


    
    for w,nameservers in data.items():
        for ns in nameservers:
            print(f"{w},{ns}")

if __name__ == "__main__":
    main()