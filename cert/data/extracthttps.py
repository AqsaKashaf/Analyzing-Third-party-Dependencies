

import sys



codes = {104: "ECONNRESET", 124: "timeout SIGTERM", 0: "okay", 1:"cert about to expire", 127:"command invalid"}




def attachRank():
    f = open("../list1m2020.csv","r")
    rank = 1
    data = {}
    for line in f:
        line = line.strip()        
        data[line] = rank
        rank += 1
    
    return data

def supportHTTPS(filename,https):
    ranks = attachRank()
    f = open(filename,"r")
    for line in f:
        line = line.strip("\n")
        if(line != ""):
            line = line.split(" ")
            code = line[1]
            website = line[0]
            rank = ranks[website]
            if(rank <= 100000 and code == "0"):
                https.add((rank,website))
    
    # print (len(supportHTTPS))
    return https


def findCodes(filename, uniqueCodes):
   
    f = open(filename,"r")
    for line in f:
        line = line.strip("\n")
        if(line != ""):
            line = line.split(" ")
            code = line[1]
            if(code not in uniqueCodes):
                uniqueCodes[code] = 0
            uniqueCodes[code] += 1
    
    f.close()
    return uniqueCodes


def findMissing(https):
    
    available = set()

    f = open("CA_Current","r")
    for line in f:
        # print(line)
        line = line.strip().split(",")
        rank = int(line[0])
        website = line[1]
        available.add((rank,website))

    f.close()
    
    count = 0
    for h in https:
        if(h not in available):
            r,w = h
            count += 1
            # print(w)

    print (count)

def main():
   
    uniqueCodes = {}
    https = set()
    filename = sys.argv[1]
   
    for i in range(30):
        # print(i)
        # uniqueCodes = findCodes(filename+ str(i), uniqueCodes)
        https = supportHTTPS(filename+str(i), https)

    # print (len(https))
   
    findMissing(https)

if __name__ == "__main__":
    main()