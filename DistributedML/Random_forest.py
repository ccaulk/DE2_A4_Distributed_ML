import ray
import tune from ray
from sklearn.datasets import fetch_covtype
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

print("Done importing")

#fetching the data
cov_type = fetch_covtype()
print(shape(cov_type.data.shape))

ray.init()
tune.run()

@ray.remote
def find_params():
    

find_params()

ray.shutdown()