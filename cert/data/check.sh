

website=$1
# echo "$website"
cmnd="echo QUIT | timeout 5 openssl s_client -connect $website:443 -status"
# echo "$cmnd"
eval dastring=\`${cmnd}\`
ret=$?
echo "$ret"
