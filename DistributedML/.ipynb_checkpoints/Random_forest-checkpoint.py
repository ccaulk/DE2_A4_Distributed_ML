import ray
import numpy as np
from ray import tune
from sklearn.datasets import fetch_covtype
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
print("Done importing")

#fetching the data
cov_type = fetch_covtype()
X = cov_type.data
Y = cov_type.target

print("Done with data collection")
#connect to the ray cluster
ray.init(include_dashboard=True)
#store data so we don't load it everytime the model is run
data_X = ray.put(X)
data_Y = ray.put(Y)

#running the model with the given hyperparameters with 3 fold cross validation 
def run_model(config):
    #model configuration
    model = RandomForestClassifier(n_estimators=config["n_estimators"], max_depth=config["max_depth"], ccp_alpha=config["ccp_alpha"])
    #3 fold cross validation
    scores = cross_val_score(model, ray.get(data_X), ray.get(data_Y), cv = 3)
    #reporting average accuracy
    accuracy = np.mean(scores)
    tune.report({"accuracy": accuracy})

#parameter space for hyperparameter tuning
param_space = {
    "max_depth": tune.grid_search([5,10,20]),
    "n_estimators" : tune.grid_search([75,100,125]),
    "ccp_alpha" : tune.grid_search([0,0.001,0.01]),
}
#running the hyperparameter tuning on the ray cluster
analysis = tune.run(
    run_model,
    config=param_space,
    mode = "max",
    metric = "accuracy"
)

# Get the best result
print("Best hyperparameters found were: ", analysis.best_config)
print("Best result was: ", analysis.best_result["accuracy"])

#shutting down
ray.shutdown()
