import subprocess
import os
import sys
from pathlib import Path

REGION_NAME= 'us-east-2'
filename=sys.argv[1]
companyName=sys.argv[2]
project=sys.argv[3]
part=sys.argv[4]
variation=sys.argv[5]
filetype=sys.argv[6]


key=os.path.join(os.getcwd(),"newec2.pem")
server="ec2-user@ec2-3-144-191-179.us-east-2.compute.amazonaws.com"
print(key)
#key="c:/Users/Kashmira/Projects/DataMoverTask/data.pem"
directory=os.path.join("/home/ec2-user/data",companyName,project,part,variation)
print(directory)

def ec2upload(filename,companyName,project,part,variation,filetype):
    
    serverhosturl="ec2-user@ec2-3-144-191-179.us-east-2.compute.amazonaws.com:~"
    print("serverhosturl",serverhosturl)
    if filetype=='a':
        path=os.path.join('data',companyName,project,part,variation,"annotation")
        
    else:
        path=os.path.join('data/',companyName,project,part,variation)
        


    serverhosturlwithpath=os.path.join(serverhosturl,path)
    directory='/home/ec2-user/data/'+companyName

    print("directory: ",directory)


    process = subprocess.Popen(["ssh","-i",key, server,'mkdir', directory],
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    stdout, stderr

    process = subprocess.Popen(["ssh","-i",key, server,'mkdir', directory+'/'+project],
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    stdout, stderr

    process = subprocess.Popen(["ssh","-i",key, server,'mkdir', directory+'/'+project+'/'+part],
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    stdout, stderr
    process = subprocess.Popen(["ssh","-i",key, server,'mkdir', directory+'/'+project+'/'+part+'/'+variation],
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    stdout, stderr
    if filetype=='a':
        process = subprocess.Popen(["ssh","-i",key, server,'mkdir', directory+'/'+project+'/'+part+'/'+variation+'/annotation'],
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        stdout, stderr


    print("serverhosturlwithpath: ",serverhosturlwithpath)
    subprocess.run(["scp","-i",key, filename, serverhosturlwithpath])

ec2upload(filename,companyName,project,part,variation,filetype)

