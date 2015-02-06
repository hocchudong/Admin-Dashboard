from swiftclient import client
import os
import json
import sys
import urllib2
import authen

#keystone = ks_client.Client(username = user,
#                            password = passwd,
#                            tenant_name = tenantName,
#                            auth_url = URL+":35357/v2.0"
#                            )
                            
#authtoken = keystone.auth_ref['token']['id']

#tenants = keystone.tenants.list()
#for item in tenants:
#    if item.name == tenantName:
#        tenantId = item.id

#storageURL = URL + ":8080/v1/AUTH_%s/" % tenantId

def get_token():
    storageURL, authtoken = client.get_auth(authen.auth_url + ':35357/v2.0',
                                              authen.username,
                                              authen.password,
                                              tenant_name = authen.tenant_name,
                                              auth_version = 2
                                             )
    return storageURL, authtoken

storageURL, authtoken = get_token()


def account_info():
    headers, containers = client.get_account(url = storageURL,
                                             token = authtoken
                                            )
    return headers, containers

def container_info(container):
    headers, objects = client.get_container(url = storageURL,
                                            token = authtoken,
                                            container = container
                                           )
    return headers, objects


def object_info(container,obj):
    headers, content = client.get_object(url = storageURL,
                                         token = authtoken,
                                         container = container,
                                         name = obj
                                        )
    return headers, content
    
    
def create_container(container):
    return client.put_container(url = storageURL,
                                token = authtoken,
                                container = container
                               )

def del_object(container,obj):
    return client.delete_object(url = storageURL,
                                token = authtoken,
                                container = container,
                                name = obj
                               )
    
def del_container(container):
    headers, objs = container_info(container)
    if len(objs) != 0:
        for i in objs:
            del_object(container,i['name'])
    return client.delete_container(url = storageURL,
                                   token = authtoken,
                                   container = container
                                  )











