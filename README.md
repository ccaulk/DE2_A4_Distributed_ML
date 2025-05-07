# DE2_A4_Distributed_ML
### Repository for the Data Engineering 2 Course at Uppsala University that is focused on distributed machine learning  
This Repository is meant to help with Assignment 4 of the Data Engineering 2 course at Uppsala University. In this assignment we are suppose to use Ray Tune to build a small 3 VM cluster on the Swedish Science cloud to run hyper parameter tunning on a Sklearn Random forest model and compare the time with 1-3 machines. This repository aims to do this task starting from 1 VM and then building the other 2 VMs from it. Hopefully.  

### Starting up 1 VM  
Initially 1 VM from the Swedish Science cloud will have to be made. From that machine the script.sh script can be run to install all the necessary packages. There are also some installations such as docker and tensorflow that can be installed with this script but are not needed (I think). For this part you will also need an API key from SSC which is not included in this repository for security reasons, but to create the other two VMs you will need a ```<some-string>_openrc.sh``` file that has your own authentication key which is obtained from SSC. Once you have the ```<some-string>_openrc.sh``` file in on your VM (mine is in the ```/home/ubuntu/``` directory) run the following commands.  
    
```source <some-string>_openrc.sh```  
```./script.sh```  

  I think the `./script.sh` command can be run anywhere or you can copy the script to the `/home/ubuntu/` directory and run it. I don't think it matters. You can also set up jupyter server from this link https://jupyter-server.readthedocs.io/en/stable/operators/public-server.html and if the command `jupyter server` is not found make sure that your `PATH` environment points to it with the following command  
  `export PATH=$PATH:~/.local/bin`  
  To connect to the notebook type `https://Floating-IP-Address:port` in search bar and ignore all warnings.  

### Setting up other VMs  
Since we will need 2 other VMs anyways, I thought it would be cool to set them up from the master VM on the swedish science cloud as done in Assignment 3. Do start up instances of 2 more VMs to run the distributed ML naviagte to the openstack folder. Go into the `Start_Workers.py` file and modify the flavor, image, network, and descriptive names in this file. Also add a security group that is open Ingress and Egress on port 6379 since this is the default port for Ray Tune. Save the file and make sure that you have run `source <some-string>_openrc.sh` before running `python3 Start_Workers.py` in the terminal. Once the instances have been created, all of the needed libraries should be installed. This may take 10-15 minutes for both VMs to be up and running.  

> [!NOTE]  
> For some reason not all the packages and dependices were installed on the second VM. In the start up you may have to specifiy its own userdata file separately.


### Distributed ML
