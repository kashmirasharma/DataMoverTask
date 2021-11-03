import boto3
from botocore.exceptions import ClientError
import os
import sys
from pathlib import Path
import xml.etree.ElementTree as ET
import datetime
from pymongo import MongoClient
import subprocess




REGION_NAME= 'us-east-2'

key="c:/Users/Kashmira/Projects/DataMoverTask/data.pem"

def ec2upload(filename,companyName,project,part,variation):
    path=os.path.join('data/',companyName,project,part,variation)
    serverhosturl=os.path.join("ubuntu@ec2-18-204-214-171.compute-1.amazonaws.com:~",path)
    subprocess.run(["scp","-i",key, filename, serverhosturl])




def s3fileupload(filepath,bucketname):
    try:
        session = boto3.Session(
        aws_access_key_id= 'AKIAXF4OGBL7KE7TS56G',
        aws_secret_access_key= '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',
        region_name= 'us-east-2',
    )
        s3 = session.resource('s3')
        bucket = s3.Bucket(bucketname)

        for subdir, dirs, files in os.walk(filepath):
            for file in files:
                full_path = os.path.join(subdir, file)
                with open(full_path, 'rb') as data:
                    response=bucket.put_object(Key=full_path[len('path')+1:], Body=data)

        s3_url = "https://{bucketname}.s3.{REGION_NAME}.amazonaws.com/{filepath}"
        return s3_url
    except ClientError as e:
        print(e)
        return False
    
## init s3 bucketname
## Create connection
## upload the data to the bucket.
## return fileurl


def makeMongoEntry(fileurl, annotation_data, annotation_class):

# create a template doc
    templatedoc={

    "file_url" : "",
    "created_at" : "",
    "created_by" : "",
    "modified_at": "",
    "modified_by": "",
    "meta_data" : {
    "bbox_annotations" : "",
    "class_annotation" : ""
    }
    }
    templatedoc["file_url"]=fileurl
    templatedoc["created_at"]=datetime.datetime.now()
    templatedoc["created_by"]="username"
    templatedoc["meta_data"]["bbox_annotations"]=annotation_data
    templatedoc["meta_data"]["class_annotation"]=list(annotation_class)

    try:
        client = MongoClient("mongodb://localhost:27017/")
        # what should be the mongodb connection server
        print("SUCCESSFULLY CONNECTED")
    except:
        print("Could not connect to Mongodb")

    mydatabase=client['admin']
    mycollection=mydatabase['AnnotationData']

    cursor=mycollection.find()
    x=mycollection.insert_one(templatedoc)





# make relevant entries to the document.
# Check if the primary key exists(check duplicates)
# if doesnt exist , insert the doc.




def read_annotations(annotationfilepath):
    tree=ET.parse(annotationfilepath)
    root=tree.getroot()
    classset=set()
    annotationlist=[]
    for item in root.findall('./object'):
        for child in item:
            annotation={}
            if child.tag=="name":
                name=child.text
                coordinates=[]
                classset.add(name)
            if child.tag=="bndbox":
                for subchild in child:
                    coordinates.append(subchild.text)
            annotation[name]=coordinates
            annotationlist.append(annotation)
    print(classset)
    return annotationlist,classset
        

#read_annotations("c:/Users/Kashmira/Projects/DataMoverTask/PhoneDirectory_web-converted_nimbus_11_Page_01.xml")   


def driver(companyName, project, part, variation):
    image_data_path = os.path.join('/home/ubuntu/data/',companyName, project, part, variation)
    annotation_path = os.path.join('/home/ubuntu/data/',companyName, project, part, variation,'annotation')

    for file in os.listdir(image_data_path):
        imagefilepath = os.path.join(image_data_path, file)
        # print("FILE IS : ",file)
        # print("imagefilepath is: ",image_data_path)
    for file in os.listdir(annotation_path):
        annotationfilepath = os.path.join(annotation_path, file)
        print("FILE IS : ",file)
        print("annotationfilepath is: ",annotationfilepath)

    #annotationfilepath = os.path.join(annotation_path, "PhoneDirectory_web-converted_nimbus_11_Page_01.xml")

    #fileurl = s3fileupload(imagefilepath, "image"/"annotations")
    fileurl = s3fileupload(imagefilepath, "s3-annotate")

    if os.path.exists(annotation_path):
        annotation_data,annotation_class = read_annotations(annotationfilepath)
    makeMongoEntry(fileurl, annotation_data,annotation_class)


companyname=sys.argv[1]
project=sys.argv[2]
part=sys.argv[3]
variation=sys.argv[4]

driver(companyname, project, part, variation)
