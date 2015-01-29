#!/usr/bin/python
import argparse
import json
import sys
import urllib2
import authen


listTenants = []
listUsers = []
listidServer=[]

def getToken(url):

    """ 
    Tra ve token cua user khi khai bao tenant
    username, password va OpenStack API URL
    
    """
    tokenRequest = urllib2.Request(url)
    tokenRequest.add_header("Content-type", "application/json")
    jsonPayload = json.dumps({'auth' : {'tenantName' : authen.tenant_name, 'passwordCredentials' : {'username' : authen.username, 'password' : authen.password}}})
    
    request = urllib2.urlopen(tokenRequest, jsonPayload)
    json_data = json.loads(request.read())
    
    request.close()
#    print "*"*100
    return json.dumps(json_data)

# module lay ve danh sanh servers tren tenant da khai bao
def getlist(url,token_xacthuc):
 
    tenantRequest = urllib2.Request(url)
    # add header 
    tenantRequest.add_header("X-Auth-Token", token_xacthuc)
  
    request = urllib2.urlopen(tenantRequest)
    json_data = json.loads(request.read())
    
    request.close()
    
    return json_data

def hypervisor():
#lay ve jsone file tu module getToken
#    print authen.auth_url
    adminToken = json.loads(getToken(authen.auth_url+":35357/v2.0/tokens"))
#print adminToken

# doc file JSON va lay ve token and tenant ID
    adminTokenID = adminToken['access']['token']['id']

    adminTokenTenantID = adminToken['access']['token']['tenant']['id']

 
    hypervisorJson = getlist(authen.auth_url+":8774/v2/"+adminTokenTenantID+"/os-hypervisors/detail",adminTokenID)

#    print hypervisorJson['hypervisors'][0]['memory_mb']
    #listHypervisors=[]
    for item in hypervisorJson['hypervisors']:
        hypervisor=[]
        hypervisor.append(item['vcpus'])
        hypervisor.append(item['vcpus_used'])
        hypervisor.append(str(item['memory_mb'])+"MB")
        hypervisor.append(str(item['memory_mb_used'])+"MB")
        hypervisor.append(str(item['local_gb'])+"GB")
        hypervisor.append(str(item['local_gb_used'])+'GB')
        hypervisor.append(item['running_vms'])
        #listHypervisors.append(hypervisor)
    return hypervisor
