

import sys



def readData(datafile):

    data = {}
    started = False

    f = open(datafile,"r")
    website = ""
    count = 0
    print("{")
    first = True
    for line in f:
        
        
        if(":{\n" in line):
            
            if(not first):
                if("ssl-certificate-errorhostname" in line or "socket-error" in line):
                    line = line.split(":")
                    line = '},\n"' + line[0].lstrip("}") +'":{\n'
                else:
                    line = line.replace("}",'},\n"')
                    line=line.replace(":{",'":{')
            else:
                line = line.strip().split(":")
                line = '"' + line[0] + '":{'
                first = False
        
        print (line)

    print("}")
    




if __name__ == "__main__":
    filename = sys.argv[1]
    readData(filename)