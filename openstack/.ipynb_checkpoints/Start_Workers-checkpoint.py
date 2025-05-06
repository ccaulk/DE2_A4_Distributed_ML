# http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html
import time, os, sys, random, re
import inspect
from os import environ as env

from  novaclient import client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session


flavor = "ssc.small" 
private_net = 'UPPMAX 2025/1-2 Internal IPv4 Network'
floating_ip_pool_name = None
floating_ip = None
image_name = "Ubuntu 22.04 - 2024.01.15"

identifier_1= 1
identifier_2 = 2

loader = loading.get_plugin_loader('password')

auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                password=env['OS_PASSWORD'],
                                project_name=env['OS_PROJECT_NAME'],
                                project_domain_id=env['OS_PROJECT_DOMAIN_ID'],
                                #project_id=env['OS_PROJECT_ID'],
                                user_domain_name=env['OS_USER_DOMAIN_NAME'])

sess = session.Session(auth=auth)
nova = client.Client('2.1', session=sess)
print ("user authorization completed.")

image = nova.glance.find_image(image_name)

flavor = nova.flavors.find(name=flavor)

if private_net != None:
    net = nova.neutron.find_network(private_net)
    nics = [{'net-id': net.id}]
else:
    sys.exit("private-net not defined.")

#print("Path at terminal when executing this file")
#print(os.getcwd() + "\n")
cfg_file_path =  os.getcwd()+'/cloud-cfg.txt'
if os.path.isfile(cfg_file_path):
    userdata = open(cfg_file_path)
else:
    sys.exit("prod-cloud-cfg.txt is not in current working directory") 

secgroups = ['default','Caleb_Caulk_Security_Group']

print ("Creating instances ... ")
instance_worker_1 = nova.servers.create(name="Caleb_Caulk_A4_worker_"+str(identifier_1), image=image, flavor=flavor, key_name='Caleb_Caulk_Key_Pair',userdata=userdata, nics=nics,security_groups=secgroups)
instance_worker_2 = nova.servers.create(name="Caleb_Caulk_A4_worker_"+str(identifier_2), image=image, flavor=flavor, key_name='Caleb_Caulk_Key_Pair',userdata=userdata, nics=nics,security_groups=secgroups)
instance_worker_1_status = instance_worker_1.status
instance_worker_2_status = instance_worker_2.status

print ("waiting for 10 seconds.. ")
time.sleep(10)

while instance_worker_1 == 'BUILD' or instance_worker_2 == 'BUILD':
    print ("Instance: "+instance_worker_1.name+" is in "+instance_worker_1_status+" state, sleeping for 5 seconds more...")
    print ("Instance: "+instance_worker_2.name+" is in "+instance_worker_2_status+" state, sleeping for 5 seconds more...")
    time.sleep(5)
    instance_worker_1 = nova.servers.get(instance_worker_1.id)
    instance_worker_1_status = instance_worker_1.status
    instance_worker_2 = nova.servers.get(instance_worker_2.id)
    instance_worker_2_status = instance_worker_2.status

#kept getting an error on line 76. Not sure why but it isn't necessary for the VM to run
# ip_address_1 = None
# print(instance_worker_1.networks.keys())
# for network in instance_worker_1.networks[private_net]:
#     if re.match('\d+\.\d+\.\d+\.\d+', network):
#         ip_address_1 = network
#         break
# if ip_address_1 is None:
#     raise RuntimeError('No IP address assigned!')

# ip_address_2 = None
# for network in instance_worker_2.networks[private_net]:
#     if re.match('\d+\.\d+\.\d+\.\d+', network):
#         ip_address_2 = network
#         break
# if ip_address_2 is None:
#     raise RuntimeError('No IP address assigned!')

# print ("Instance: "+ instance_worker_1.name +" is in " + instance_worker_1_status + " state" + " ip address: "+ ip_address_1)
# print ("Instance: "+ instance_worker_2.name +" is in " + instance_worker_2_status + " state" + " ip address: "+ ip_address_2)
