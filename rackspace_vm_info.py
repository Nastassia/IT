''' .RAX_CRED file needed in your home directory for script to run.
.RAX_CRED file should contain at least:
[rackspace_cloud]
username= <username>
api_key= <api key> '''

#!/usr/bin/env python

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import sys
import os.path
import csv
from datetime import datetime
import pytz
from dateutil.parser import parse

if os.path.isfile(os.environ['HOME']+"/.RAX_CRED"):
        with open(os.environ['HOME']+"/.RAX_CRED") as file:
                lines = file.readlines()
                RACKSPACE_USER=lines[1].split("=")[1].rstrip()
                RACKSPACE_KEY=lines[2].split("=")[1].rstrip()
else:
        print "'.RAX_CRED' file needed in homedir."
        sys.exit(1)


cls = get_driver(Provider.RACKSPACE)
driver = cls(RACKSPACE_USER, RACKSPACE_KEY, region='ord')

servers = []
for node in driver.list_nodes():

        vm = {}
        vm['server_name'] = str(node.name)
        vm['server_id']= str(node.id)
        if node.public_ips == []:
                vm['public_ip'] = []
                vm['private_ip'] = []
        else:
                vm['public_ip']= str(node.extra['access_ip'])
                vm['private_ip']= str(node.private_ips[0])
        td = str(node.extra['metadata']['rax:reboot_window'])
        begin = parse(td.split(';')[0])
        end = parse(td.split(';')[1])
        fmt = '%m-%d-%Y %I:%M:%S %p'
        begin_local = begin.astimezone(pytz.timezone('US/Eastern'))
        end_local = end.astimezone(pytz.timezone('US/Eastern'))
        vm['reboot_start_time']= begin_local.strftime(fmt)
        vm['reboot_end_time'] = end_local.strftime(fmt)
        vm['region']= 'ord'
        servers.append(vm)

print len(servers)

# write data to csv

with open('rackspace_reboots.csv', 'wb') as file:
        header = ['server_name', 'server_id', 'public_ip', 'private_ip', 'reboot_start_time', 'reboot_end_time', 'region']
        wr = csv.DictWriter(file, fieldnames=header)
        wr.writeheader()
        for node in servers:
                wr.writerow(node)

file.close()
