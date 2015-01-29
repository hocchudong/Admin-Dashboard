import os
import authen
import json
import sys
import urllib2
from keystoneclient.v2_0 import client

class colors:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'

keystone = client.Client(username=authen.username,password=authen.password,
                        tenant_name=authen.tenant_name, auth_url=authen.auth_url+":35357/v2.0")
dicTenInstan={}
listTenantsName=[]
listTenantsId=[]
dicTenantToken={}

tenants = keystone.tenants.list()
for item in tenants:
    if item.name == "demo":
        listTenantsName.append(item.name)
        listTenantsId.append(item.id)

for item in tenants:
    if item.name == "admin":
        listTenantsName.append(item.name)
        listTenantsId.append(item.id)   
    if item.name !="service" and item.name !="invisible_to_admin" :
        listTenantsName.append(item.name)
        listTenantsId.append(item.id)
def getTenantToken(idTenant):

    keystone = client.Client(username=authen.username,password=authen.password,
                    tenant_id=idTenant, auth_url=authen.auth_url+":35357/v2.0")
    token= keystone.auth_ref['token']['id']
    return token

def getlistTenantsName():
    return listTenantsName

def getidTenantsName():
    return listTenantsId
        
   
 # Ham lay ve danh sach cac may ao
def getlist(url,token_xacthuc):
   

    tenantRequest = urllib2.Request(url)
    tenantRequest.add_header("X-Auth-Token",token_xacthuc)
  
    request = urllib2.urlopen(tenantRequest)
    json_data = json.loads(request.read())
    
    request.close()
    
    return json.dumps(json_data)




# Ham reboot cac may ao
def reboot(url,token_xacthuc):
    
    requestReboot = urllib2.Request(url)
    requestReboot.add_header("X-Auth-Token", token_xacthuc)
    requestReboot.add_header("Content-type", "application/json")

    jsonPayload = json.dumps({"reboot":{"type":"SOFT"}})
    request = urllib2.urlopen(requestReboot, jsonPayload)

def pause(url,token_xacthuc):
    
    requestReboot = urllib2.Request(url)
    requestReboot.add_header("X-Auth-Token", token_xacthuc)
    requestReboot.add_header("Content-type", "application/json")

    jsonPayload = json.dumps({"pause":"null"})
    request = urllib2.urlopen(requestReboot, jsonPayload)


def unpause(url,token_xacthuc):
    
    requestReboot = urllib2.Request(url)
    requestReboot.add_header("X-Auth-Token", token_xacthuc)
    requestReboot.add_header("Content-type", "application/json")

    jsonPayload = json.dumps({"unpause":"null"})
    request = urllib2.urlopen(requestReboot, jsonPayload)
    
def checkstatus(url,token_xacthuc):

    checkRequest = urllib2.Request(url)
    checkRequest.add_header("X-Auth-Token",token_xacthuc)
  
    request = urllib2.urlopen(checkRequest)
    json_data = json.loads(request.read())
    
    request.close()
    
    return json_data
    


def listServerFuntion():
        # Khai bao danh sach cac id server
    
        # Khai bao danh sach thong tin cac server
    listServers =[]

        # vong lap cac phan tu trong danh sach tenant name
    for item in listTenantsName:
            # xac thuc 
        keystone = client.Client(username=authen.username,password=authen.password,
                    tenant_name=item, auth_url=authen.auth_url+":35357/v2.0")
        token= keystone.auth_ref['token']['id']
        tenants= keystone.tenants.list()
        for item2 in tenants:
            if item2.name==item:
                idTenant=item2.id

                listServersJson = json.loads(getlist(authen.auth_url+":8774/v2/"+idTenant+"/servers/detail",token))
                
                for item in listServersJson['servers']:                    
                    dicservers={}
                    dicservers['idTenant']= item2.id
                    dicservers['nameTenant']= item2.name
                    dicservers['tenmayao'] = item['name']
                    dicservers['idmayao'] = item['id']
                    listServers.append(dicservers)             
    return listServers

def check_status(idTenant,idmayao):
    adminTokenID = getTenantToken(idTenant)
    link=authen.auth_url+":8774/v2/"+idTenant+"/servers/"+idmayao
    check= checkstatus(link,adminTokenID)
    return check['server']['status']
    
    
    
def rebootmayao(idTenant,idmayao):
    adminTokenID = getTenantToken(idTenant)
    link=authen.auth_url+":8774/v2/"+idTenant+"/servers/"+idmayao+"/action"
    reboot(link,adminTokenID)

def pausemayao(idTenant,idmayao):
    adminTokenID = getTenantToken(idTenant)
    link=authen.auth_url+":8774/v2/"+idTenant+"/servers/"+idmayao+"/action"
    pause(link,adminTokenID)

def unpausemayao(idTenant,idmayao):
    adminTokenID = getTenantToken(idTenant)
    link=authen.auth_url+":8774/v2/"+idTenant+"/servers/"+idmayao+"/action"
    unpause(link,adminTokenID)

def shutdown(url,token_xacthuc):
    requestReboot = urllib2.Request(url)
    requestReboot.add_header("X-Auth-Token", token_xacthuc)
    requestReboot.add_header("Content-type", "application/json")
    jsonPayload = json.dumps({"os-stop": "null"})
    request = urllib2.urlopen(requestReboot, jsonPayload)
    
def shutdownmayao(idTenant,idmayao):
    adminTokenID = getTenantToken(idTenant)
    link=authen.auth_url+":8774/v2/"+idTenant+"/servers/"+idmayao+"/action"
    shutdown(link,adminTokenID)
    
def start(url,token_xacthuc):
    requestReboot = urllib2.Request(url)
    requestReboot.add_header("X-Auth-Token", token_xacthuc)
    requestReboot.add_header("Content-type", "application/json")
    jsonPayload = json.dumps({"os-start": "null"})
    request = urllib2.urlopen(requestReboot, jsonPayload)

def batmayao(idTenant,idmayao):
    adminTokenID = getTenantToken(idTenant)
    link=authen.auth_url+":8774/v2/"+idTenant+"/servers/"+idmayao+"/action"
    start(link,adminTokenID)
    

def startmayao(idTenant,idmayao):
    a = check_status(idTenant,idmayao)
    if a == 'PAUSED':
        return unpausemayao(idTenant,idmayao)
    else:
        return batmayao(idTenant,idmayao)

def reboot_tenant(idTenant,lst_instance):
    for i in lst_instance:
        a = check_status(idTenant,i)
        if a == 'ACTIVE':
            rebootmayao(idTenant,i)

            
def start_tenant(idTenant,lst_instance):
    for i in lst_instance:
        a = check_status(idTenant,i)
        if a == 'SHUTOFF':
            startmayao(idTenant,i)
        else:
            pass

def shutdown_tenant(idTenant,lst_instance):
    for i in lst_instance:
        a = check_status(idTenant,i)
        if a != 'SHUTOFF':
            shutdownmayao(idTenant,i)
        else:
            pass

    