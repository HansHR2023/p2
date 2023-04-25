# p2
Harbour Transportation

In the Harbour and Transport project a simulation of a self driving car works on /simulations/car/control_client/hardcoded_client.py

This file listens through a socket wrapper to the data from /simulations/car/world.py and steers the car over the track. At the same time data is writtten to the file default.samples
By renaming the file, the experiments can be saved foro later use: the training of the model. 

When starting the simulation with ./test_client.sh there are 2 options:
- l for lidar: data generated has 16 features and 1 label (steering angle as speed is fixed) 
- s for sonar: data generated has 3 features and 1 label (steering angle as speed is fixed)

In /notebooks are 5 notebooks where the model is built to train 2 models:
- a model optimized for lidar
- a model optimized for sonar

/notebooks/Harbour_Transport_3.ipynb is the nb used for the experiments. In nb 4 and 5 are the first steps for using PyTorch Lightning in connection with ML flow. This is not finished.

MLflow is used to save all experiments that otherwise would have been done in the experiment matrix. All data is saved in /notebooks/mlruns 

The models are saved in /simpylc and called by agent.sh
This file calls /simulations/car/control_client/better_than_tesla.py and the simulation can be run with the trained models.
