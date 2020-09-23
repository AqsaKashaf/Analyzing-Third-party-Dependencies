
import sys, json, tldextract
import collections


errorMsgs = ["socket-error[Errno -5] No address associated with hostname","socket-error[Errno -5] No address associated with hostname", "socket-errortimed out","socket-error[Errno 111] Connection refused","socket-error[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:645)", "socket-error[Errno 113] No route to host", "socket-error[SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure (_ssl.c:645)","socket-error[Errno -2] Name or service not known","socket-errorEOF occurred in violation of protocol (_ssl.c:645)","socket-error[SSL: TLSV1_ALERT_INTERNAL_ERROR] tlsv1 alert internal error (_ssl.c:645)","socket-error[SSL: TLSV1_UNRECOGNIZED_NAME] tlsv1 unrecognized name (_ssl.c:645)","socket-error[Errno -3] Temporary failure in name resolution","socket-error[SSL: UNKNOWN_PROTOCOL] unknown protocol (_ssl.c:645)","socket-error[Errno 104] Connection reset by peer","socket-error[Errno 101] Network is unreachable","socket-error_ssl.c:629: The handshake operation timed out","socket-error[SSL: TLSV1_ALERT_PROTOCOL_VERSION] tlsv1 alert protocol version (_ssl.c:645)","socket-error[SSL: BAD_SIGNATURE] bad signature (_ssl.c:645)","socket-error[SSL: UNSUPPORTED_PROTOCOL] unsupported protocol (_ssl.c:645)","socket-error[Errno 22] Invalid argument","socket-error[SSL: SSL_NEGATIVE_LENGTH] dh key too small (_ssl.c:645)","socket-error[SSL: UNEXPECTED_MESSAGE] unexpected message (_ssl.c:645)","socket-error[SSL: EXCESSIVE_MESSAGE_SIZE] excessive message size (_ssl.c:645)","socket-error[SSL: SSLV3_ALERT_BAD_CERTIFICATE] sslv3 alert bad certificate (_ssl.c:645)","socket-error[SSL: UNKNOWN_CIPHER_RETURNED] unknown cipher returned (_ssl.c:645)","socket-error[Errno 107] Transport endpoint is not connected"]



def attachRank():
    ranks = {}
    r = 1
    f = open("../list1m2020.csv","r")
    for line in f:    
        ranks[line.strip()] = r
        r+=1
    
    return ranks

def readData(filename,ocspData, crlData, caData, caUrlData):

    ranks = attachRank()
    f = open(filename, "r")
    data = json.load(f)
    
    
    # print(len(data.keys()))
    notprint = False
    for i in data.keys():
        val = i
        for err in errorMsgs:
            if(err in val):
                val = val.replace(err," ")
        
        # websites = val.split(":")
        # website = ""
        crl = ""
        ocsp = ""
        ca = ""
        caURL = ""
        
        # if(len(websites) > 1):
        #     website = websites[-1]
        # else:
        #     website=websites[0]
        website = data[i]["website"]
        try:
            caURL = set(data[i]["caIssuers"])
        
        except KeyError as e:
            # print(f"ocsp error {website}")
            caURL =  "none"
     
        try:
            ocsp = set(data[i]["OCSP"])
        
        except KeyError as e:
            # print(f"ocsp error {website}")
            ocsp =  "none"
        
        try:
            crl = set(data[i]["crlDistributionPoints"])
        
        except KeyError as e:
            # print(f"crl error {website}")
            crl = "none"
        
        try:
            caIssuer = data[i]["issuer"]
            ca = ""
            for l in caIssuer:
               if("organizationName" in l[0]):
                   ca = l[0][1]
            
            # print(website, ca)

        except KeyError as e:
            # print(f"issuer error {website}")
            caIssuer = "none"
        
        website = website.strip()
        if(website in ranks and ranks[website] <= 100000):
            rank = ranks[website]
            if((rank,website) not in ocspData):
                ocspData[(rank,website)] = ocsp
            
            if((rank,website) not in crlData):
                crlData[(rank,website)] = crl
            
            if((rank,website) not in caData):
                caData[(rank,website)] = ca
            
            if((rank,website) not in caUrlData):
                caUrlData[(rank,website)] = caURL
            

    return ocspData, crlData, caData, caUrlData
        
        
        
def main():
    
    global errorMsgs
    
    

    filename = sys.argv[1]
    uniqueCAs = set()
    ocspData = {}
    crlData = {}
    caData = {}
    caUrlData = {}
    for i in range(50):
        
        # print(i)
        # 
        ocspData, crlData, caData, caUrlData = readData(filename+str(i),ocspData, crlData, caData, caUrlData)
        
    for (i,j),k in caData.items():
        print(str(i) + "," + j + "," + k)
        
    # for (i,j), k in ocspData.items():
    #     print(str(i) + "," + j + "," + " ".join(k))
        
    # for (i,j), k in crlData.items():
    #     print(str(i) + "," + j + "," + " ".join(k))
    
    # caUrlData = collections.OrderedDict(sorted(caUrlData.items()))
    # for (i,j), k in caUrlData.items():
            # ca = list(k)[0]
            # # print (ca)
            # tld = tldextract.extract(ca)
            # tld = tld.domain + "." + tld.suffix
            # uniqueCAs.add(tld)
        
       
            # print(str(i) + "," + j + "," + " ".join(k))    

    # print(len(uniqueCAs))
# # 
#     for i in uniqueCAs:
#         print(i)
        

    
    


        
        # print(website, data[i]["issuer"])



                    




if __name__ == "__main__":
    main()