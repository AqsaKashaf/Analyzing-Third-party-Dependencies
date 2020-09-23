

import sys, tldextract



def main():
    datafile= sys.argv[1]

    ns = set()

    f = open(datafile,"r")
    for line in f:
        line=line.strip().split(",")
        # print(line)
        ns.add(line[2])


    for n in ns:
        print(n)



if __name__ == "__main__":
    main()