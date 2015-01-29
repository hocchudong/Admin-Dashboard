import os
import authen
from keystoneclient.v2_0 import client

class colors:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'

#Xac thuc
keystone = client.Client(username=authen.username,password=authen.password,
                        tenant_name=authen.tenant_name, auth_url=authen.auth_url+':35357/v2.0/')

#Cac tinh nang
menu = {}
menu['1']="Danh sach Tenant"
menu['2']="Danh sach User"
menu['3']="Danh sach Role"
menu['4']="Danh sach Service"
menu['5']="Danh sach Endpoint"
menu['6']="Tao moi, xoa Tenants"
menu['7']="Tao moi, xoa Roles"
menu['8']="Tao moi, xoa User"
menu['9']="Exit"

os.system('clear')

def listTenantsFuntion():
    
    listTenants=[]
    
         
    #Respone tenant-list json file
    tenants = keystone.tenants.list()
    for item in tenants:
        tenant=[]
        if item.enabled:
            a="True"
        else:
            a="False"
        tenant.append(item.id)
        tenant.append(item.name)
        tenant.append(a)
        listTenants.append(tenant)

    return listTenants
        
        

#module list user   
def listUsersFuntion():
    listUsers=[]
    
    #Respone user-list json file
    users = keystone.users.list()

    for item in users:
        user=[]

        if item.enabled:
            a="True"
        else:
            a="False"
        user.append(item.id)
        user.append(item.username)
        user.append(a)
        listUsers.append(user)
    return listUsers


#module list roles
def listRolesFuntion():
    listRoles=[]    
     
    #Respone role-list json file
    roles = keystone.roles.list()
    for item in roles:
        role=[]
        role.append(item.id)
        role.append(item.name) 
        listRoles.append(role)
    return listRoles

#module list services
def listServicesFuntion():
    listServices=[]
    
    #Respone services-list json file
    services = keystone.services.list()
    for item in services:
        service=[]
        service.append(item.id)
        service.append(item.name)
        service.append(item.type)
        service.append(item.description)
        listServices.append(service)
    return listServices

#module list Endpoints
def listEndpointsFuntion():
    listEndpoints=[]

    #Respone endpoint-list json file
    endpoints = keystone.endpoints.list()
    for item in endpoints:
        endpoint=[]
        endpoint.append(item.id)
        endpoint.append(item.service_id)
        endpoint.append(item.internalurl)
        endpoint.append(item.adminurl)
        endpoint.append(item.publicurl) 
        listEndpoints.append(endpoint)                                                   
    return listEndpoints
   
#module add tenant
def addTenantFuntion():
    tenant_name= raw_input("Ten tenant> ")
    description= raw_input("Description> ")
    try:
        keystone.tenants.create(tenant_name=tenant_name,
                                description=description, enable= True)
    except Exception, Argument:
        print colors.YELLOW+"Sai cu phap hoac tennant da ton tai!"+colors.END, Argument
    else:
        print "OK! ban da them tennant "+colors.RED+tenant_name+colors.END+ " thanh cong!"
        listTenantsFuntion()

#module delete tanent
def delTenantFuntion():
    listTenantsFuntion()
    print colors.GREEN+"\n\n-----Nhap ten tenant ban muon xoa-----"+colors.END
    tenant_name=raw_input("> ")
    #Respone tenant-list json file
    tenants = keystone.tenants.list()
    try:
        my_tenant = [x for x in tenants if x.name==tenant_name][0]
    
        keystone.tenants.delete(my_tenant.id)
    except Exception, Argument:
        print colors.YELLOW+"Tenant ban nhap vao khong ton tai!"+colors.END, Argument
    else:
        print "OK! ban da xoa tenant "+colors.RED+tenant_name+colors.END+"thanh cong!"

#module add Role   
def addRoleFuntion():
    role_name = raw_input("Ten role> ")
    try:
        keystone.roles.create(role_name)
    except Exception, Argument:
        print colors.YELLOW+"Sai cu phap hoac roles da ton tai!"+colors.END, Argument
    else:
        print "OK! ban da them role "+colors.RED+role_name+colors.END+ " thanh cong!"
        listRolesFuntion()

#module delte Role
def deleteRoleFuntion():
    listRolesFuntion()
    print colors.GREEN+"-----Nhap ten role ban muon xoa-----"+colors.END
    role_name = raw_input("> ")
    roles =  keystone.roles.list()
    try:
        my_role = [x for x in roles if x.name==role_name][0]

        keystone.roles.delete(my_role.id)
    except Exception, Argument:
        print colors.YELLOW+"Role ban nhap vao khong dung!"+colors.END, Argument
    else:
        print "OK! ban da xoa role "+colors.RED+role_name+colors.END+" thanh cong!"

#module add User
def addUserFuntion():
    a= True
    user_name=raw_input("Nhap ten user> ")
    user_pass=raw_input("Nhap password> ")
    tenant_name=raw_input("User thuoc tennant > ")
    tenants = keystone.tenants.list()
    try:
        my_tenant = [x for x in tenants if x.name==tenant_name][0]
        my_user = keystone.users.create(name=user_name,password=user_pass,tenant_id=my_tenant.id)
    except Exception, Argument:
        print colors.YELLOW+"Tenant ban nhap vao khong ton tai hoac user da ton tai!"+colors.END, Argument
        a= False
    else:
        print "OK, ban da them user "+colors.RED+user_name+colors.END+" thanh cong!"
        listUsersFuntion()
        print colors.YELLOW+'''\n\nChu y: Role mac dinh cho user la _member_
Ban co muon thay doi khong(yes or no)'''+colors.END

    while a:
        yes_no=raw_input('>')
        if yes_no=='yes':
            role_name=raw_input('Nhap role name > ')
            roles= keystone.roles.list()
            try:
                my_roles = [x for x in roles if x.name==role_name][0]
                keystone.roles.add_user_role(my_user.id,my_roles.id,my_tenant.id)
            except Exception, Argument:
                print colors.YELLOW+"Role ban nhap vao khong ton tai !"+colors.END, Argument
            else:
                print "OK!!!"
            break
        elif yes_no=='no':
            break
        else:
            print "Moi chon lai"

#module delete User
def deleteUserFuntion():
    listUsersFuntion()
    print "-----Nhap ten user ban muon xoa-----"
    user_name = raw_input(">")
    users =  keystone.users.list()
    try:
        my_user = [x for x in users if x.name==user_name][0]

        keystone.users.delete(my_user.id)
    except Exception, Argument:
        print "Ten user ban nhap vao khong dung!", Argument
    else:
        print "OK! ban da xoa user thanh cong!"   


#menu
"""while True:
    options=menu.keys()
    options.sort()
    print "                          ___________________________"

    for entry in options:
        print "                         |"+ colors.RED+entry+colors.END+"    ","%20s" %menu[entry],"|"
        print "                         |___________________________|"
    selection=raw_input("\nPlease Select: ")
    if selection =='1':     
        listTenantsFuntion()
        
    elif selection == '2':
        listUsersFuntion()
        
    elif selection == '3':
        listRolesFuntion()

    elif selection == '4':      
        listServicesFuntion()

    elif selection == '5':        
        listEndpointsFuntion()

    elif selection == '6':
        while True:
            print '''
     ___________________
    |1.  Tao moi tenant |
    |-------------------|    
    |2.  Xoa tenant     |
    |-------------------|
    |3.  Exit           |
    |___________________|
            '''
            select=raw_input("> ")
            if select=='1':
                addTenantFuntion()
            elif select=='2':
                delTenantFuntion()
            elif select =="3":
                os.system('clear')
                break
            else:
                print colors.YELLOW+ "Ban chon khong dung, moi chon lai!"+colors.END

    elif selection == '7':
        while True:
            print '''
     ___________________
    |1.  Tao moi role   |
    |-------------------|    
    |2.  Xoa role       |
    |-------------------|
    |3.  Exit           |
    |___________________|
            '''
            select=raw_input("> ")
            if select=='1':
                addRoleFuntion()
            elif select =='2':
                deleteRoleFuntion()
            elif select =="3":
                os.system('clear')
                break
            else:
                print colors.YELLOW+ "Ban chon khong dung, moi chon lai!"+colors.END

    elif selection == '8':
        while True:
            print '''
     ___________________
    |1.  Tao moi user   |
    |-------------------|    
    |2.  Xoa user       |
    |-------------------|
    |3.  Exit           |
    |___________________|
            '''
            select=raw_input("> ")
            if select=='1':
                addUserFuntion()
            elif select=='2':
                deleteUserFuntion()
            elif select =="3":
                os.system('clear')
                break
            else:
                print colors.YELLOW+ "Ban chon khong dung, moi chon lai!"+colors.END


    elif selection == '9':
      break
    else:
        print colors.YELLOW+ "Ban chon khong dung, moi chon lai!"+colors.END

"""

