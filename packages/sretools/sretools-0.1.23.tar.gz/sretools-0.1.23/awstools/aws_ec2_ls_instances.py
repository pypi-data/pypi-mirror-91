#!/usr/bin/python3

import json
from subprocess import Popen, PIPE
import sys
import boto3
import re
from sretools import SimpleTable

result=list()

def clrline() :
    print('\b'*30,end="")
    print(' '*30,end="")
    print('\b'*30,end="",flush=True)

for region in ["us-east-1","us-east-2","us-west-1","us-west-2","ca-central-1","eu-west-1","eu-west-2","eu-west-3"] :
    clrline()
    print(region,end="",flush=True)
    client = boto3.client('ec2',region_name=region)
    response = client.describe_instances()
    for reservation in response["Reservations"]:
        for inst in reservation["Instances"]:
            insttype = inst["InstanceType"]
            instid = inst["InstanceId"]
            launchtime = inst["LaunchTime"].strftime("%m/%d/%Y %H:%M:%S")
            az = inst["Placement"]["AvailabilityZone"]
            iip = inst.get("PrivateIpAddress",'n/a')
            pip = inst.get("PublicIpAddress",'n/a')
            status = inst["State"]["Name"]
            tags=list()
            for t in inst.get("Tags",[{"Key":"Name","Value":"n/a"}]) :
                if t["Key"] == "Name" :
                    tags.append(t["Value"])
            tag=",".join(tags)
            if tag == "":
                tag = "n/a"
            result.append([tag,instid,iip,pip,insttype,launchtime,az,status])
clrline()

st = SimpleTable(data=sorted(result,key=lambda x:(x[-1],x[0])),header=re.split(r"\s+","tag instance_id private_ip public_ip inst_type launch_time(UTC) az status"))
print(st)

