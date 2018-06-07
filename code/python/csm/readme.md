# Physics model 

## Run model
- `python simulation_2ball.py`: original simple 2ball experiment 
- `python simulation_3ball.py`: experiment with teleports 
- `python simulation_teleport.py`: experiment with 3 balls 
- all of these call `model.py`
- for each you can set some parameters: 
	+ which trials to run 
	+ whether or not to record the data
	+ whether or not to animate 
	+ noise: set how much noise is applied to balls' motions in the counterfactuals 

## Make videos 

```
bash make_video.sh experiment trial
```
- experiment options: 
	+ '2ball'
	+ 'teleport'
	+ '3ball'
- trial options: 
	+ note that it uses 0 indexing (i.e. trial 0 here is trial 1 in the experiment)
