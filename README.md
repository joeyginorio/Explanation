# Using counterfactual simulation to construct compositional explanations
---
## Python Code Summary
The model is written in python and can be found in /code/python/. There are four main scripts:
- Events.py
- Counterfactuals.py
- Explanations.py
- Experiment.py
  
Code Dependency: Events.py -> Counterfactuals.py -> Explanations.py -> Experiment.py    

#### Events.py
This script contains the Events class, which contains all the methods for generating physics simulations (including animations).  
#### Counterfactuals.py
This script contains the Counterfactuals class. It uses the Events class, in addition to newly defined methods, to run counterfactual simulations and construct a tree-like representation of all possible counterfactual worlds for a given physics simulation.  
#### Explanations.py
This script contains the Explanations class. Uses the Counterfactuals class, in addition to newly defined methods, to construct and score explanations coming from the tree-like representation defined in Counterfactuals.py.
#### Experiment.py
This script is a tester class, used to get data from the model on pre-defined trials. Trials are defined as methods in the class, which specify the parameters of the simulation to be tested.  

---
## Tutorial
To use this code, you want to use and write code in Experiment.py, which interfaces with the computational model.  

Here's how to run a trial from the experiment:

1. Open terminal at the home directory of the repo, then switch to the python source code by using this command:
```
cd code/python
```
2. Start an ipython console by typing this command into terminal:
```
ipython
```
3. Now we can run the model. Here are a few examples of animations for counterfactual simulations on trial 7. 
```python
# Initialize an object from the experiment class
E = Experiment()

# Run trial 7 animation, actual world
E.trial7(animate=True, seq='1',save=False)

# Run trial 7 animation, ignoring first collision
E.trial7(animate=True, seq='01',save=False)

# Run trial 7 animation, ignoring second collision
E.trial7(animate=True, seq='10',save=False)

# Run trial 7, no animation, but receiving the model's results (explanations in order from best-worst)
results = E.trial7()

# Print the top explanation
print results[0]

```



