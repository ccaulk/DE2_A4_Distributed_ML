import ray
from ray import tune
import time
import numpy as np
from sklearn.datasets import fetch_covtype
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate
from sklearn.model_selection import cross_val_score
print("Done importing")

#fetching the data
cov_type = fetch_covtype()
X = cov_type.data
Y = cov_type.target

#connect to the ray cluster
ray.init()

def run_model(config):
    model = RandomForestClassifier(n_estimators=config["n_estimators"], max_depth=config["max_depth"], ccp_alpha=config["ccp_alpha"])
    scores = cross_val_score(model, X, Y, cv = 3)
    accuracy = np.mean(scores)
    tune.report({"accuracy": accuracy})

param_space = {
    "max_depth": tune.grid_search([5,10,15]),
    "n_estimators" : tune.grid_search([75,100,125]),
    "ccp_alpha" : tune.grid_search([0,.5,1]),
}

analysis = tune.run(
    run_model,
    config=param_space,
    mode = "max",
    metric = "accuracy"
)

# Get the best result
print("Best hyperparameters found were: ", analysis.best_config)
print("Best result was: ", analysis.best_result["accuracy"])



ray.shutdown()