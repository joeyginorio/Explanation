# Joey Velez-Ginorio
# BMM Summer Project w/ Tobi

"""
	This script uses counterfactuals to build relations between events
	represented by a physics engine.
"""


"""
    E <-- B <--- A

    - A collides B CAUSING B collides E AFFECTS E through the gate    
	- A collides B 

    1. A collides B
    B collides E
    E through gate

    Counterfactuals:

    1. No A collides B
    E not through gate

    2. No B collides E
    A collides E
    E through gate
		
		A
		|
	E---B

	- A collides B CAUSING E through the gate
	- A collides B PREVENTING B collides E CAUSING E through the gate 

	Full
	1. A Collides B
	2. E not through gate

	No A collides B
	1. B collides E
	2. E though gate

	No 

	Preventing is what happens in the counterfactual and not in the actual
	Causing is what happens in the actual and not in the counterfactual


	Rules for CF Relation Building:

	1. Simulate actual world, get e_summary()
	- Store current event e, at time t
	- Store next event e_next, at time t+1
	
	2. Simulate counterfactual world
	- Ignore event e, at time t
	- Store next event e_next_cf, at time t+1

	3. Build Relations 

	If next event e_next == e_next_cf
	- If e_next and e_next_cf happen at same time t+1, e MADE NO DIFFERENCE e_next
	- If e_next and e_next_cf happen at different times t+1, e AFFECTED e_next

	If next event e_next != e_next_cf
	- If e_next_cf not in e_summary, e CAUSED e_next
	- If e_next_cf in e_summary, 

	- If next event at t+1 is not in summary list of events, then event at time t 
	prevented event at time t+1
	- If next event at t+1 


"""

