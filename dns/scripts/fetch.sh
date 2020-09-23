
mkdir results

for i in {0..9}
do
    echo "NUMBER: $i"
    ssh "dep$i" "cp ~/https/blah /proj/cloudmigration-PG0/akashaf/cert/https$i"

done

ssh dep0 "zip  /proj/cloudmigration-PG0/akashaf/cert/https.zip /proj/cloudmigration-PG0/akashaf/cert/https*"
scp dep0:/proj/cloudmigration-PG0/akashaf/cert/https.zip results/

unzip -o ./results/https.zip -d ./results/
# mv ./results/dns.zip ../results/dns.zip

# cat ./results/* > resDNS

