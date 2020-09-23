

import sys



def attachRank():
    f = open("../list1m2020.csv","r")
    rank = 1
    data = {}
    for line in f:
        line = line.strip()        
        data[line] = rank
        rank += 1
    
    return data

def missing(ranks, items):

    count = 0
    websites = []
    for w,r in ranks.items():
        if(r <= 100000):
            if(w not in items):
                websites.append(w)
                count += 1
    

    return count, websites
    




def main():

    datafile = sys.argv[1]
    f = open(datafile,"r")
    items = {}
    error = []
    for line in f:
        line = line.strip().split(",")
        rank = line[0]
        website = line[1]
        if(website not in items):
            items[website] = set()
        items[website].add(line[2])
        if(line[2] == "error"):
            error.append(website)


    missing = set()

    for w in error:
        if(len(items[w]) == 1):
            missing.add(w)
    # print(count)

    print(len(missing), len(error))




if __name__ == "__main__":
    main()