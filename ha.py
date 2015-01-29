import psutil
cpu = psutil.cpu_count()
ram = psutil.virtual_memory()
disk = psutil.disk_usage('/')
#print cpu
a= (float(ram.total))/(1024*1024)
#print '%0.2f' %a
b= (float(ram.used))/(1024*1024)
#print '%0.2f' %b
c= (float(disk.total))/(1024*1024)
#print '%0.2f' %c
d= (float(disk.used))/(1024*1024)
print str('%0.2f' %a) + ' '+ str('%0.2f' %b) +' '+ str('%0.2f' %c) +' '+ str( '%0.2f' %d)
