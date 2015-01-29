from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse


def home(request):
    import sys_function
    tena = sys_function.listTenantsFuntion()
    hd_tena = ['ID', 'Name', 'Enable']
    user = sys_function.listUsersFuntion()
    hd_user = ['ID', 'Name', 'Enable']
    serv = sys_function.listServicesFuntion()
    hd_serv = ['ID', 'Name', 'Type', 'Description']
    endp = sys_function.listEndpointsFuntion()
    hd_endp = ['ID', 'Service ID','InternalURL', 'AdminURL', 'PublicURL']
    role = sys_function.listRolesFuntion()
    hd_role = ['ID', 'Name']
    return render_to_response('index.html', {'tena': tena, 'hd_tena': hd_tena, 'user': user, 'hd_user': hd_user, 'serv': serv, 'hd_serv': hd_serv, 'endp': endp, 'hd_endp': hd_endp, 'role': role, 'hd_role': hd_role })


def performance(request):
    return render_to_response('performance.html')

def instances(request):
    import infomations
    infos = infomations.listServerFuntion()
    name = infomations.getlistTenantsName()
    id_tenant = infomations.getlistIdTenant()
    hd = ['Hostname','ID','Int IP','Image ID','Status','Actions']
    kq = zip(name, infos, id_tenant)
    if request.method == "POST":
        if 'reboot' in request.POST:
            import actions
            instanceid = request.POST['instanceid']
            tenantid = request.POST['tenantid']
            actions.rebootmayao(tenantid,instanceid)
            return render(request,'instances.html' ,{'hd': hd, 'kq': kq})
        elif 'start' in request.POST:
            import actions
            instanceid = request.POST['instanceid']
            tenantid = request.POST['tenantid']
            actions.startmayao(tenantid,instanceid)
            return render(request,'instances.html' ,{'hd': hd, 'kq': kq})
        
        elif 'shutdown' in request.POST:
            import actions
            instanceid = request.POST['instanceid']
            tenantid = request.POST['tenantid']
            actions.shutdownmayao(tenantid,instanceid)
            return render(request,'instances.html' ,{'hd': hd, 'kq': kq})
        elif 'pause' in request.POST:
            import actions
            instanceid = request.POST['instanceid']
            tenantid = request.POST['tenantid']
            actions.pausemayao(tenantid,instanceid)
            return render(request,'instances.html' ,{'hd': hd, 'kq': kq})
        elif 'reboot_tenant' in request.POST:
            import actions
            tenant_id = request.POST['reboot_tenant']
            lst_id_tenant = infomations.getlistIdTenant()
            instances_id = infomations.listIdServerFuntion()
            lst = zip(lst_id_tenant, instances_id)
            for i, j in lst:
                if i == tenant_id:
                    lst_instance = j
                    break
            actions.reboot_tenant(tenant_id,lst_instance)
            return render(request,'instances.html' ,{'hd': hd, 'kq': kq})
        elif 'reboot_all' in request.POST:
            import actions
            lst_id_tenant = infomations.getlistIdTenant()
            instances_id = infomations.listIdServerFuntion()
            lst = zip(lst_id_tenant, instances_id)
            for i,j in lst:
                actions.reboot_tenant(i,j)
            return render(request,'instances.html' ,{'hd': hd, 'kq': kq})
        elif 'start_all' in request.POST:
            import actions
            lst_id_tenant = infomations.getlistIdTenant()
            instances_id = infomations.listIdServerFuntion()
            lst = zip(lst_id_tenant, instances_id)
            for i,j in lst:
                actions.start_tenant(i,j)
            return render(request,'instances.html' ,{'hd': hd, 'kq': kq})
        elif 'shutdown_all' in request.POST:
            import actions
            lst_id_tenant = infomations.getlistIdTenant()
            instances_id = infomations.listIdServerFuntion()
            lst = zip(lst_id_tenant, instances_id)
            for i,j in lst:
                actions.shutdown_tenant(i,j)
            return render(request,'instances.html' ,{'hd': hd, 'kq': kq})
    else:
        return render(request,'instances.html', {'hd': hd, 'kq': kq})
