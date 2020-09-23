



import sys,os
import collections

def attachRank():
    ranks = {}
    r = 1
    f = open("../list1m2020.csv","r")
    for line in f:    
        ranks[line.strip()] = r
        r+=1
    
    return ranks



def readFile(filename):
    f = open(filename,"r")
    website = ""
    started = False
    ranks = attachRank()
    staple = {}
    for line in f:
        line = line.strip()
        try:
            if(started):
                if ("OCSP Response Status: successful" in line):
                    rank = ranks[website]
                    if(rank <= 100000):
                        key = rank,website
                        staple[key] = "yes"
                
                elif("output is OCSP response: no response sent" in line or "output is Error: Command failed:" in line):
                    rank = ranks[website]
                    if(rank <= 100000):
                        key = rank,website
                        staple[key] = "no"
                    
                elif("Next Update:" in line or line == ""):
                    started = False
                
            

            elif(line != ""):
                website = line
                started = True
        except KeyError:
            pass
    return staple


def main():
    directory = sys.argv[1]
    files = os.listdir(directory)
    data = {}
    for f in files:
        # print(filename+str(i))
        f = directory + "/" + f
        data = {**readFile(f),**data}


    sdata = collections.OrderedDict(sorted(data.items()))
    for (i,j),k in sdata.items():
        print (f"{i},{j},{k}")
            



if __name__ == "__main__":
    main()