#!/usr/bin/env python
import json, re, sys, os, json, time, logging, requests, urllib3
from requests.structures import CaseInsensitiveDict
urllib3.disable_warnings()
from requests.structures import CaseInsensitiveDict
import subprocess
from subprocess import call, check_output

VAULT_ADDR = os.getenv('VAULT_ADDRR')
VAULT_TOKEN = os.getenv('SSH_TOKEN') #This gets the vault token from the ephemeral build container

#MAKE SURE THE AWS IS UP TO VERSION 2 ON THE BUILD CONTAINER
#GET THE DEFAULT VPC ID
outfile_vars="vars"

lab_vars='lab_vars.py'
import lab_vars
from lab_vars import *

outfile_vars="vars"
sg_name=name

#1 - Create a Key Pair
keypair_name=name
outfile_key_pair = 'keypair_name' + '.json'

#Write the var to the vault
import json, re, sys, os, json, subprocess, time, logging, requests, urllib3
from subprocess import call, check_output
from requests.structures import CaseInsensitiveDict
urllib3.disable_warnings()


#Import Lab Vars
lab_vars='lab_vars.py'
import lab_vars
from lab_vars import *

#Inject the vault var vals into the ephemeral oci build container

VAULT_ADDR = os.getenv('VAULT_ADDR')
VAULT_TOKEN = os.getenv('SSH_TOKEN')
#VAULT_TOKEN = os.getenv('VAULT_TOKEN')
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/cisco-fso-labs/" + name + "/" + "key_name"
headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"
#data = f'{{"token": "{TOKEN}"}}'
data_json = {"key_name": name }
resp = requests.post(url, headers=headers, json=data_json)
print(resp.status_code)


#Create the keypair
create_keypair='aws ec2 create-key-pair --key-name' + " " +  "{}".format(name) + " " + '--region' + " " + "{}".format(region) + " " + '--availability-zone' + " " + "{}".format(az)

#2 - CREATE THE NEW VPC01 AND GET VPCID
outfile = 'aws-vpc.json'
#cmd_deploy='aws ec2 create-vpc --region' + " " + "{}".format(region) + " " + '--cidr-block 10.10.0.0/16 --tag-specifications' + " " + "'ResourceType=vpc,Tags=[{Key=Name,Value=trainee1}]'"
cmd_deploy='aws ec2 create-vpc --region' + " " + "{}".format(region) + " " + '--cidr-block 10.0.0.0/16 --tag-specifications' + " " + "'ResourceType=vpc,Tags=[{Key=Name,Value=" + "{}".format(name) + '}]'"" + "'"
output = check_output("{}".format(cmd_deploy), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile, 'w') as my_file:
    my_file.write(output)
with open(outfile) as access_json:
    read_content = json.load(access_json)
    question_access = read_content['Vpc']
    replies_access = question_access['VpcId']
    vpcid = replies_access
    print(vpcid)
    vpcid_var=('vpcid=' + "'" + "{}".format(vpcid) + "'")
    print(vpcid_var)

with open(outfile_vars, 'a+') as my_file:
    my_file.write(vpcid_var + "\n")


#3- CREATE THE MGMT 512 SUBNET -  Interface Index 1 for Controllers. Learned that if you try to change this to default interface it requires a disconnect from SSH
outfile_subnet_MGMT = 'aws-subnet-MGMT.json'
cmd_subnet_MGMT='aws ec2 create-subnet --vpc-id' + " " + "{}".format(vpcid) + " " + '--region' + " " + "{}".format(region) + " " + '--availability-zone' + " " + "{}".format(az) + " " + '--cidr-block 10.0.1.0/24 --tag-specifications' + " " "'ResourceType=subnet,Tags=[{Key=Name,Value=SUBNET_MGMT}]'"
print(cmd_subnet_MGMT)
output = check_output("{}".format(cmd_subnet_MGMT), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_subnet_MGMT, 'w') as my_file:
    my_file.write(output)
with open (outfile_subnet_MGMT) as access_json:
    read_content = json.load(access_json)
    question_access = read_content['Subnet']
    replies_access = question_access['SubnetId']
subnetid_MGMT = replies_access
print(subnetid_MGMT)

subnetid_MGMT_var=('subnetid_MGMT=' + "'" + "{}".format(subnetid_MGMT) + "'")

with open(outfile_vars, 'a+') as my_file:
    my_file.write(subnetid_MGMT_var + "\n")


#4- CREATE THE TUNNEL SUBNET for vpn0 - transport TUNNEL for interface VPN0
outfile_subnet_TUNNEL = 'aws-subnet-TUNNEL.json'
cmd_subnet_TUNNEL='aws ec2 create-subnet --vpc-id' + " " + "{}".format(vpcid) + " " + '--region' + " " + "{}".format(region) + " " + '--availability-zone' + " " + "{}".format(az) + " " + '--cidr-block 10.0.2.0/24 --tag-specifications' + " " "'ResourceType=subnet,Tags=[{Key=Name,Value=SUBNET_TUNNEL}]'"
print(cmd_subnet_TUNNEL)
output = check_output("{}".format(cmd_subnet_TUNNEL), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_subnet_TUNNEL, 'w') as my_file:
    my_file.write(output)
with open (outfile_subnet_TUNNEL) as access_json:
    read_content = json.load(access_json)
    question_access = read_content['Subnet']
    replies_access = question_access['SubnetId']
    subnetid_TUNNEL = replies_access
    print(subnetid_TUNNEL)
    subnetid_TUNNEL_var=('subnetid_TUNNEL=' + "'" + "{}".format(subnetid_TUNNEL) + "'")

with open(outfile_vars, 'a+') as my_file:
    my_file.write(subnetid_TUNNEL_var + "\n")


#5- CREATE THE CLUSTER SUBNET
outfile_subnet_CLUSTER = 'aws-subnet-CLUSTER.json'
cmd_subnet_CLUSTER='aws ec2 create-subnet --vpc-id' + " " + "{}".format(vpcid) + " " + '--region' + " " + "{}".format(region) + " " + '--availability-zone' + " " + "{}".format(az) + " " + '--cidr-block 10.0.3.0/24 --tag-specifications' + " " "'ResourceType=subnet,Tags=[{Key=Name,Value=SUBNET_CLUSTER}]'"
print(cmd_subnet_CLUSTER)
output = check_output("{}".format(cmd_subnet_CLUSTER), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_subnet_CLUSTER, 'w') as my_file:
    my_file.write(output)
with open (outfile_subnet_CLUSTER) as access_json:
    read_content = json.load(access_json)
    question_access = read_content['Subnet']
    replies_access = question_access['SubnetId']
subnetid_CLUSTER = replies_access
print(subnetid_CLUSTER)

subnetid_CLUSTER_var=('subnetid_CLUSTER=' + "'" + "{}".format(subnetid_CLUSTER) + "'")

with open(outfile_vars, 'a+') as my_file:
    my_file.write(subnetid_CLUSTER_var + "\n")


#5 - CREATE INTERNET GATEWAY
outfile_ig = 'aws-ig.json'
cmd_ig='aws ec2 create-internet-gateway --region' + " " + "{}".format(region) + " " + '--tag-specifications' + " " + "'ResourceType=internet-gateway,Tags=[{Key=Name,Value=IG}]'"
print(cmd_ig)
output = check_output("{}".format(cmd_ig), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_ig, 'w') as my_file:
    my_file.write(output)
with open (outfile_ig) as access_json:
    read_content = json.load(access_json)
    print(read_content)
    question_access = read_content['InternetGateway']
    print(question_access)
    replies_access = question_access['InternetGatewayId']
    print(replies_access)
igid = replies_access
print(igid)

igid_var=('igd=' + "'" + "{}".format(igid) + "'")

with open(outfile_vars, 'a+') as my_file:
    my_file.write(igid_var + "\n")

#6 - Attach Internet Gateway to the VPC
outfile_ig_attach_log = 'ig_attach_log.json'
cmd_ig_attach='aws ec2 attach-internet-gateway' + " " + '--region' + " " + "{}".format(region) + " " + '--internet-gateway-id' + " " + "{}".format(igid) + " " + '--vpc-id' + " " + "{}".format(vpcid)
print(cmd_ig_attach)
output = check_output("{}".format(cmd_ig_attach), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
#Do we need to add any var here to the vars.py??


# 7 - Get the route table id for the default route table for the new vpc
outfile_get_vpc_rt_id='get-vpc-rt-id.json'
get_vpc_rt_id='aws ec2 describe-route-tables' + " " + '--region' + " " + "{}".format(region) + " " + '--filters \"Name=vpc' + '-' + 'id,Values=' + "{}".format(vpcid) + '"' + " " + '--query "RouteTables[]"'
output = check_output("{}".format(get_vpc_rt_id), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_get_vpc_rt_id , 'w') as my_file:
    my_file.write(output)
with open (outfile_get_vpc_rt_id ) as access_json:
    read_content=json.load(access_json)
    question_access=read_content[0]
    replies_access=question_access['Associations']
    replies_data=replies_access[0]
    def_vpc_rt_id=replies_data['RouteTableId']
    print(def_vpc_rt_id)


def_vpc_rt_id_var=('def_vpc_rt_id=' + "'" + "{}".format(def_vpc_rt_id) + "'")
with open(outfile_vars, 'a+') as my_file:
    my_file.write(def_vpc_rt_id_var + "\n")

#Tag the default rout table --resources   --tags Key=Name,Value=DEFAULT_RT

#8 - aws ec2 create-tags to identify the vpc default route table
tag_def_vpc_rt='aws ec2 create-tags --resources --region' + " " + "{}".format(region) + " " + " " + "{}".format(def_vpc_rt_id) + " " + '--tags Key=Name,Value=DEFAULT_RT_' + "{}".format(name)
output = check_output("{}".format(tag_def_vpc_rt), shell=True).decode().strip()
print("Output: \n{}\n".format(output))

#9 - Add a new route to the default vpc route table requires the default vpc route table id and associated and the default gatewayid
outfile_ass_rt = 'ass_rt.json'
ass_rt_default_rt='aws ec2 create-route' + " " + '--region' + " " + "{}".format(region) + " " + '--route-table-id' + " " + "{}".format(def_vpc_rt_id) + " " + '--destination-cidr-block 0.0.0.0/0 --gateway-id' + " " + igid
output = check_output("{}".format(ass_rt_default_rt), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_ass_rt, 'w') as my_file:
    my_file.write(output)

#10 - Create MGMT Route Table
outfile_rt_MGMT = 'aws-rt-MGMT.json'
cmd_rt_MGMT='aws ec2 create-route-table --vpc-id' + " " + "{}".format(vpcid) + " " + '--region' + " " + "{}".format(region) + " " + '--tag-specifications' + " " + "'ResourceType=route-table,Tags=[{Key=Name,Value=MGMT_RT}]'"
print(cmd_rt_MGMT)
output = check_output("{}".format(cmd_rt_MGMT), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_rt_MGMT, 'w') as my_file:
    my_file.write(output)
with open (outfile_rt_MGMT) as access_json:
    read_content = json.load(access_json)
    question_access = read_content['RouteTable']
    replies_access = question_access['RouteTableId']
rt_MGMT_id = replies_access
print(rt_MGMT_id)

rt_MGMT_id_var=('rt_MGMT_id=' + "'" + "{}".format(rt_MGMT_id) + "'")
with open(outfile_vars, 'a+') as my_file:
    my_file.write(rt_MGMT_id_var + "\n")

#11 - Create TUNNEL Route Table
outfile_TUNNEL_rt = 'aws-rt-TUNNEL.json'
cmd_TUNNEL_rt='aws ec2 create-route-table --vpc-id' + " " + "{}".format(vpcid) + " " + '--region' + " " + "{}".format(region) + " " + '--tag-specifications' + " " + "'ResourceType=route-table,Tags=[{Key=Name,Value=TUNNEL_RT}]'"
print(cmd_TUNNEL_rt)
output = check_output("{}".format(cmd_TUNNEL_rt), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_TUNNEL_rt, 'w') as my_file:
    my_file.write(output)
with open (outfile_TUNNEL_rt) as access_json:
    read_content = json.load(access_json)
    question_access = read_content['RouteTable']
    replies_access = question_access['RouteTableId']
rt_TUNNEL_id = replies_access
print(rt_TUNNEL_id)

rt_TUNNEL_id_var=('rt_rt_id=' + "'" + "{}".format(rt_TUNNEL_id) + "'")
with open(outfile_vars, 'a+') as my_file:
    my_file.write(rt_TUNNEL_id_var + "\n")


#11 - Create CLUSTER Route Table
outfile_CLUSTER_rt = 'aws-rt-CLUSTER.json'
cmd_CLUSTER_rt='aws ec2 create-route-table --vpc-id' + " " + "{}".format(vpcid) + " " + '--region' + " " + "{}".format(region) + " " + '--tag-specifications' + " " + "'ResourceType=route-table,Tags=[{Key=Name,Value=CLUSTER_RT}]'"
print(cmd_CLUSTER_rt)
output = check_output("{}".format(cmd_CLUSTER_rt), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_CLUSTER_rt, 'w') as my_file:
    my_file.write(output)
with open (outfile_CLUSTER_rt) as access_json:
    read_content = json.load(access_json)
    question_access = read_content['RouteTable']
    replies_access = question_access['RouteTableId']
rt_CLUSTER_id = replies_access
print(rt_CLUSTER_id)

rt_CLUSTER_id_var=('rt_rt_id=' + "'" + "{}".format(rt_CLUSTER_id) + "'")
with open(outfile_vars, 'a+') as my_file:
    my_file.write(rt_CLUSTER_id_var + "\n")


#12 - ASSOCIATE THE MGMT ROUTE TABLE WITH THE MGMT SUBNET
outfile_ass_MGMT_sub = 'ass_rt_MGMT_sub.json'
ass_rt_MGMT_sub='aws ec2 associate-route-table --region' + " " + "{}".format(region) + " " + '--route-table-id' + " " + "{}".format(rt_MGMT_id) + " " + '--subnet-id' + " " + "{}".format(subnetid_MGMT)
print(ass_rt_MGMT_sub)
output = check_output("{}".format(ass_rt_MGMT_sub), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_ass_MGMT_sub, 'w') as my_file:
    my_file.write(output)


#ASSOCIATE THE TUNNEL ROUTE TABLE WITH THE TUNNEL SUBNET
outfile_ass_TUNNEL_sub = 'ass_TUNNEL_sub.json'
ass_rt_TUNNEL_sub='aws ec2 associate-route-table' + " " + '--region' + " " + "{}".format(region) + " " + '--route-table-id' + " " + "{}".format(rt_TUNNEL_id) + " " +  '--subnet-id' + " " + "{}".format(subnetid_TUNNEL)
print(ass_rt_TUNNEL_sub)
output = check_output("{}".format(ass_rt_TUNNEL_sub), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_ass_TUNNEL_sub, 'w') as my_file:
    my_file.write(output)

#ASSOCIATE THE CLUSTER ROUTE TABLE WITH THE CLUSTER SUBNET
outfile_ass_rt_CLUSTER_sub = 'ass_rt_CLUSTER_sub.json'
ass_rt_CLUSTER_sub='aws ec2 associate-route-table' + " " + '--region' + " " + "{}".format(region) + " " + '--route-table-id' + " " + "{}".format(rt_CLUSTER_id) + " " +  '--subnet-id' + " " + "{}".format(subnetid_CLUSTER)
print(ass_rt_CLUSTER_sub)
output = check_output("{}".format(ass_rt_CLUSTER_sub), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(outfile_ass_rt_CLUSTER_sub, 'w') as my_file:
    my_file.write(output)



#Add a route to this TUNNEL route table that is to the internet gateway
#Destination 0.0.0.0/0 Target: The igw for the VPC
#aws ec2 create-route --route-table-id rtb-22574640 --destination-cidr-block 0.0.0.0/0 --gateway-id igw-c0a643a9
#Need the RT ID and the GatewayID
#aws ec2 create-route --route-table-id rt_rt_id --destination-cidr-block 0.0.0.0/0 --gateway-id igid
#aws ec2 create-route --route-table-id rtb-037f6e0a9f82e1d9e --destination-cidr-block 0.0.0.0/0 --gateway-id igw-0cd42c1b9fdd2bc6d
print("Creating TUNNEL Route Table Route and Associating with Gateway")
cmd_create_TUNNEL_rt_route='aws ec2 create-route --route-table-id' + " " + "{}".format(rt_TUNNEL_id) + " " + '--destination-cidr-block 0.0.0.0/0' + " " + '--gateway-id' + " " + igid
print(cmd_create_TUNNEL_rt_route)
output = check_output("{}".format(cmd_create_TUNNEL_rt_route), shell=True).decode().strip()
print("Output: \n{}\n".format(output))

#13 - Create a Security Group
out_file_sg_TUNNEL='outfile-sg-TUNNEL.json'
cmd_security_group='aws ec2 create-security-group --group-name --region' + " " + "{}".format(region) + " " + " " + "{}".format(sg_name) + " " + '--description' + " " + "{}".format(sg_name) + " " + '--vpc-id' + " " + "{}".format(vpcid)
output = check_output("{}".format(cmd_security_group), shell=True).decode().strip()
print("Output: \n{}\n".format(output))
with open(out_file_sg_TUNNEL, 'w') as my_file:
    my_file.write(output)
with open (out_file_sg_TUNNEL) as access_json:
    read_content = json.load(access_json)
    question_access = read_content['GroupId']
    TUNNEL_sg_id=question_access
    TUNNEL_sg_id_var=('TUNNEL_sg_id=' + "'" + "{}".format(TUNNEL_sg_id) + "'")
    print(TUNNEL_sg_id_var)
with open(outfile_vars, 'a+') as my_file:
    my_file.write(TUNNEL_sg_id_var + "\n")

#Create inbound rule on the security group to allow SSH
#aws ec2 authorize-security-group-ingress --group-id sg-1234567890abcdef0 --protocol tcp --port 22 --cidr 0.0.0.0/0
auth_inbound_ssh='aws ec2 authorize-security-group-ingress --region' + " " + "{}".format(region) + " " + '--group-id' + " " "{}".format(TUNNEL_sg_id) + " " + '--protocol tcp --port 22 --cidr 0.0.0.0/0'
output = check_output("{}".format(auth_inbound_ssh), shell=True).decode().strip()
print("Output: \n{}\n".format(output))


#VAULT SECTION

#Write vpcid  to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/cisco-fso-labs/" + name + "/" + "vpcid"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"vpcid": vpcid }

resp = requests.post(url, headers=headers, json=data_json)
print(resp.status_code)


#3 Write the subnetid_TUNNEL to the vault

url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/cisco-fso-labs/" + name + "/" + "subnetid_TUNNEL"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"subnetid_TUNNEL": subnetid_TUNNEL }

resp = requests.post(url, headers=headers, json=data_json)
print(resp.status_code)

#4 Write the subnetid_MGMT to the vault

url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/cisco-fso-labs/" + name + "/" + "subnetid_MGMT"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"subnetid_MGMT": subnetid_MGMT }

resp = requests.post(url, headers=headers, json=data_json)
print(resp.status_code)

#5 Write the igid to the vault

url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/cisco-fso-labs/" + name + "/" + "igid"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"igid": igid }

resp = requests.post(url, headers=headers, json=data_json)
print(resp.status_code)

#10 - Write rt_MGMT_id to the vault

url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/cisco-fso-labs/" + name + "/" + "rt_MGMT_id"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"rt_MGMT_id": rt_MGMT_id }

resp = requests.post(url, headers=headers, json=data_json)
print(resp.status_code)

#11 - Write rt_tunnel_id to the vault
url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/cisco-fso-labs/" + name + "/" + "rt_tunnel_id"

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"rt_TUNNEL_id": rt_TUNNEL_id }

resp = requests.post(url, headers=headers, json=data_json)
print(resp.status_code)

#13 - Write the TUNNEL_sg_id to the vault

url = "http://prod-vault.devops-ontap.com:8200/v1/concourse/cisco-fso-labs/" + name + "/" + "TUNNEL_sg_id"
print(url)

headers = CaseInsensitiveDict()
headers["X-Vault-Token"] = VAULT_TOKEN
headers["Content-Type"] = "application/json"

#data = f'{{"token": "{TOKEN}"}}'
data_json = {"TUNNEL_sg_id": TUNNEL_sg_id }

resp = requests.post(url, headers=headers, json=data_json)
print(resp)
print(resp.status_code)
print(name)

#Add in Here Allocate EIPs and write to vault
#aws ec2 allocate-address