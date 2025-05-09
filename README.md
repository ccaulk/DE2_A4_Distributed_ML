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
> For some reason not all the packages and dependices were installed on the second VM. In the `Start_Workers.py` file you may have to specifiy its own userdata file separately/ add another userdata defined varaible.


### Distributed ML
Once all the VMs are set up, on the head node you will want to run the following command  
`ray start --head --port=6379`  
This will start a ray cluster head node, then on the two workers you will want to run the command  
`ray start --address=<head-node-address>:6379`  
This will start up the ray cluster for the distributed machine learning. Run the command  
`ray status`  
to see the status of the ray cluster. The code is located on the path `DE2_A4_Distributed_ML/DistributedML` and the Random_Forest.py file will run hyperparameter tuning on a Random Forest model using exhaustive grid search over the parameter space. The dataset used is https://www.kaggle.com/c/forest-cover-type-prediction and the model is trying to predict the forest coverage type. Since this dataset is about 550,000x54 it is fairly large and to load the data it takes approximately 241 MB. It's not huge but it is noticeable. When running Ray Tune (https://docs.ray.io/en/master/index.html) with hyperparameter tuning grid search, everytime a new hyperparameter combination is tested the data is copied in memory and wasn't removed. Since we were running this on smaller VMs this means after a few tuning trials there would be an OOM (out of memory error). So, to solve this `ray.put()` and `ray.get()` are used to put the data in object_store_memory so we can store it once and continuously retrieve the data without replicating it for every hyperparameter combination. 
> [!NOTE]  
> Even with `ray.put()` and `ray.get()` you may run into an issue with tuning when max_depth = None and ccp_alpha > 0. I ran into an OOM error with these settings and I think it may be because the depth of the tree expands until every node is a leaf node and this can take up a lot of space to store the tree. Pruning may add more complexity, but I'm unsure, but with these settings the ray cluster may still experience an OOM error.

Once in the correct directory run
` python3 Random_Forest.py`  
to run the distributed ML hyperparameter tuning. The time will depend on the size of the VMs connected and the number of CPUs. 

### Adding more VMs/ VM set up
To add more VMs to the cluster you can create one login to it and run the script.sh with just the python3 and pip installations and the packages they install. So you can comment out docker, pytorch, and openstack. Then run  
`./script.sh`  
to install everything and run  
`ray start --address=<head-node-address>:6379`  
to add more nodes to the cluster. 
