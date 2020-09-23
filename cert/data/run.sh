
div=2500

for i in {0..39}
do
    echo "NUMBER: $i"
    
    # ssh "dep$i" "pkill screen & rm -rf ~/https"
    # rsync -r ./* "dep$i: ~/https"
    # # # ssh "dns$i" "bash ~/dns/setupDNS.sh"
    # start=$(($i*$div))
    # entries=$(($i*$div+$div))
    # ssh "dep$i" "screen -d -m python3 ~/https/checkHTTPS.py ~/https/list1m2020.csv ~/https/blah $start $entries"
    # scp ./https/appToModel.groovy "idc$i:~/code/src/appToModel.groovy"
    # result=$(ssh "wd$i" "pgrep screen" 2>&1)
    # # echo "$result"
    # if [ -n "$result" ]; then
    #     echo "$result"
    # else
    #     echo "no screen running"
    # fi
    # python3 scripts/extractCert.py "./results/proj/cloudmigration-PG0/akashaf/cert/resCERTdiff16-20$i" > "results/certdiff16-20Json$i"
    # scp ./src/main.py "idc$i:~/code/src/main.py"
    # scp ./runScripts/run.sh "utah$i:~/code/runScripts/run.sh"
    python3 extractCert.py "../results/proj/cloudmigration-PG0/akashaf/cert/resCERT20missing2$i" > ."./results/proj/cloudmigration-PG0/akashaf/cert/certjson20_v2$i"
done