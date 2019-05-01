import numpy as np
import pandas as pd
reward_state = [[[1],[2],[3]],[[4],[5],[6]],[[7],[8],[9]]]
print(reward_state[0][0][0])

for i in range(len(reward_state)):# here should have a sort finish time 
	new = reward_state[i][np.lexsort(reward_state[:,:0:].T)]