import subprocess
import os
import sys

REGION_NAME= 'us-east-2'

key="c:/Users/Kashmira/Projects/DataMoverTask/data.pem"

def ec2upload(filename,companyName,project,part,variation,filetype):
    if filetype=='a':
        path=os.path.join('data',companyName,project,part,variation,"annotation")
        print(path)
    else:
        path=os.path.join('data/',companyName,project,part,variation)
        print(path)
    
    serverhosturl=os.path.join("ubuntu@ec2-18-204-214-171.compute-1.amazonaws.com:~",path)
    subprocess.run(["scp","-i",key, filename, serverhosturl])


filename=sys.argv[1]
companyName=sys.argv[2]
project=sys.argv[3]
part=sys.argv[4]
variation=sys.argv[5]
filetype=sys.argv[6]
ec2upload(filename,companyName,project,part,variation,filetype)

