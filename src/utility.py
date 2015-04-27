
import os
import socket

class Utility:
	''' class utility '''
    def __init__(self):
        # save the os name for utest to mock it.
        self.os_name = os.name;


    def get_host_name(self):
        '''
        [public] get the hostname of current machine.
        '''
        return socket.gethostname();
    
    def get_ip_list(self):
        '''
        [public] get the ip list of current machine.
        sometimes it always return "127.0.0.1".
        '''
        #hostname, aliaslist, ipaddrlist
        try:
            host = socket.gethostbyname_ex(self.get_host_name());
            
            if len(host) < 3:
                raise Exception("failed to get ip list: %s" %(host));
            
            return host[2];
        except:
            return [];

