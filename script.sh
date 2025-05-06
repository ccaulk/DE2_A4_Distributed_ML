#updating
sudo apt update
#updgrading
sudo apt -y upgrade
#installing python
sudo apt install python3
#installing pip
sudo apt install python3-pip
#installing jupyter-core for notebooks
sudo apt -y install jupyter-core

#installing docker
#curl -fsSL https://get.docker.com -o get-docker.sh
#sudo sh get-docker.sh
#sudo groupadd docker
#sudo usermod -aG docker $USER
#newgrp docker

#installing open app client to create other VMs from this one
sudo apt -y install python3-openstackclient
sudo apt -y install python3-novaclient
sudo apt -y install python3-keystoneclient

#install python packages
pip install pandas
pip install numpy
pip install -U scikit-learn
pip install -U "ray[default,tune,train,data]"
pip install jupyter
#don't need tensorflow
#python3 -m pip install 'tensorflow[and-cuda]'

#showing installations 
python3 -c "import pandas as pd; print('Pandas Version:',pd.__version__)"
python3 -c "import numpy as np; print('Numpy Version:', np.__version__)"
python3 -c "import sklearn; print('Sklearn Versions:',sklearn.show_versions())"
#didn't need tensor flow
#python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
#lists all installations
pip list

#check the python version
echo python version:
python3 --version
#check the pip version
echo pip verison:
pip --version

#checking docker versions
#docker --version
#docker compose version

#checking that open stack client was installed correctly
openstack server list
openstack image list
