import pxssh
import getpass

def tainguyen():
    try:
        tainguyen=""
        s = pxssh.pxssh()
        s.login ('172.16.69.70', 'root', 'PTCC@!2o015')
        s.sendline('python ha.py')
        s.prompt()
        file = open("perfor.txt", "w")
        file.write(s.before)
        file.close()
        file =  open("perfor.txt","r")       
        caulenh= file.readline()
        tainguyen= file.readline() 
        s.logout()

    except pxssh.ExceptionPxssh, e:
        print "pxssh failed on login."
        print str(e)
    return tainguyen