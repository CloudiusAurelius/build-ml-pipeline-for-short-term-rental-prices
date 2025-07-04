#!/bin/bash

echo "Running mlflow to optimize Hyperparemters."
mlflow run . \
-P steps=train_random_forest \
-P hydra_options="modeling.random_forest.max_features=0.1,0.33,0.5,0.75,1 modeling.max_tfidf_features=10,15,30 modeling.random_forest.min_samples_leaf=3,4,5 --m"
echo "Run complete."
#-P hydra_options="-m modeling.random_forest.max_features=0.1,0.33,0.5,0.75,1"

