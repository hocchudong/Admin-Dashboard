from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse
#import re
#from django.db.models import Q



#def normalize_query(query_string,
#    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
#    normspace=re.compile(r'\s{2,}').sub):
#    return [normspace('',(t[0] or t[1]).strip()) for t in findterms(query_string)]
#
#def get_query(query_string, search_fields):
#    query = None # Query to search for every search term
#    terms = normalize_query(query_string)
#    for term in terms:
#        or_query = None # Query to search for a given term in each field
#        for field_name in search_fields:
#            q = Q(**{"%s__icontains" % field_name: term})
#            if or_query is None:
#                or_query = q
#            else:
#                or_query = or_query | q
#        if query is None:
#q            query = or_query
#        else:
#            query = query & or_query
##    return query

#def search_for_something(request):
#    query_string = ''
#    found_entries = None
#    if ('q' in request.GET) and request.GET['q'].strip():
#        query_string = request.GET['q']
#        entry_query = get_query(query_string, ['field1', 'field2', 'field3'])
#        found_entries = Model.objects.filter(entry_query).order_by('-something')

#    return render_to_response('result.html',
#            { 'query_string': query_string, 'found_entries': found_entries },
#            context_instance=RequestContext(request)
#        )





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
    import performance
    import hypervisor
    a = performance.tainguyen()
    lst = a.split()
    hd = ['RAM (total)', 'RAM (use)', 'Storage (total)', 'Storage (use)']
    lst2 = hypervisor.hypervisor()
    hd2 = ['CPU (total)','CPU (use)','RAM (total)', 'RAM (use)','Storage (total)', 'Storage (use)', 'Instances']
    return render_to_response('performance.html',{'hd': hd, 'lst': lst, 'hd2': hd2, 'lst2': lst2})

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


def containers(request):
    import swift_test
    acc_info ,containers = swift_test.account_info()
    hd = ['Name', 'Objects', 'Size']
    if request.method == "POST":
        if 'del_container' in request.POST:
            name = request.POST['del_container']
            swift_test.del_container(name)
            return render(request,'swift/containers.html', {'hd': hd, 'containers': containers})
        elif 'create_con' in request.POST:
            name = request.POST['con_name']
            swift_test.create_container(name)
            return render(request,'swift/containers.html', {'hd': hd, 'containers': containers})
    return render(request,'swift/containers.html', {'hd': hd, 'containers': containers})
    
def objects(request):

    return render(request,'swift/objects.html')
    
    
    
    
    
    
    
    
    
    