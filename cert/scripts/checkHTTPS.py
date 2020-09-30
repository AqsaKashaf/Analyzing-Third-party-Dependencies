import os
import sys
import subprocess
import time


filename = sys.argv[1]
f = open(filename, 'r')

outputfile = sys.argv[2]

start = int(sys.argv[3])
entries = int (sys.argv[4])

flag = False
count = 0 
for line in f:
	try:
		if(count >= start + entries):
			break
		if(count >= start):
			# print(line,count)
			line = line.strip('\n')
			output = subprocess.check_output(["bash", 'https/check.sh',line])
			# print(output)
			output = str(output,"utf-8")

			f = open(outputfile,"a")
			f.write(line + " " + output + "\n")
			f.close()
	except subprocess.CalledProcessError as e:
		f = open(outputfile,"a")
		f.write(line + ",error\n")
		f.close()
		print ("Oops error for website", line, e)
	count += 1


