from test_env import Servers
from test_brain import DeepQNetwork
import numpy as np
import pandas as pd

global s_info
global t_info
global total_price
global s_state

def read_file():
	global s_info
	global t_info
	# server information
	server_file = pd.read_csv('server.csv')
	server_file.columns=["Col1","Col2","Col3"]
	 
	s_info = server_file[["Col1","Col2","Col3"]]
	s_info = np.array(s_info)

	# task information
	task_file = pd.read_csv('task.csv')
	task_file.columns=["Col1","Col2","Col3","Col4","Col5"]
	 
	t_info = task_file[["Col1","Col2","Col3","Col4","Col5"]]
	t_info = np.array(t_info)

	# add more data into task information
	t_info = t_info[:,1:]

	a = np.zeros((len(t_info), 6))
	t_info = np.hstack((t_info, a))
	for i in range(len(t_info)):
		t_info[i][4] = t_info[i][1] + np.random.randint(0,10)
		t_info[i][5] = t_info[i][0]
		t_info[i][6] = t_info[i][1]
		t_info[i][8] = t_info[i][0]

	return s_info.shape[0]

def run_server():
	global s_info
	global t_info
	global total_price
	global s_state

	step = 0 #keep record which step I am in
	for episode in range(500):
		# initialize environment
		env = Servers()
		env.server_state(s_info)
		# print(s_state)
		# observation = s_state
		for i in range(len(t_info)):
			# if step is less than 20, then choose random server
			if i < 20:
				action1 = np.random.randint(0, 18)
			# else choose from action values
			else:
				action1 = RL.choose_server(observation1)# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			
			Resource_used, reward1, Resource_used_= env.server_step(task_info, action1)

			RL.store_transition1(Resource_used, action1, reward1, Resource_used_)


			# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

			# if step is less than 20, then choose random queue
			if i < 20:
				action2 = np.random.randint(0, 9)
			# else choose from action values
			else:
				action2 = RL.choose_vm(observation2)# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


			vm_state, reward2, vm_state_ = env.vm_step(task_info, action1, action2)
			RL.store_transition2(vm_state, action1, action2, reward2, vm_state_)

			# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


			# if step is less than 20, then choose random start time
			if i < 20:
				action3 = np.random.randint(0, 24)
			# else choose from action values
			else:
				action3 = RL.choose_time(observation3)# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

			time_state, reward3, price_cal, time_state_ = env.time_step(self, task_info, action1, action2, action3)
			RL.store_transition3(time_state, atcion1, action2, action3, reward3, time_state_)

			# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

			if (i > 200) and (i % 5 == 0): #start to learn when transition is bigger than 200 and learn every 5 steps
				RL.learn()

			observation = observation_

			# final price
			total_price += price
		# see if NN is improved
		print(total_price)


if __name__ == "__main__":
	total_price = 0
	num_servers = read_file()
	env = Servers()
	RL = DeepQNetwork(num_servers,
					env.n_features
					# learning_rate=0.01,
					# reward_decay=0.9,
					# e_greedy=0.9,
					#replace_target_iter=200,
					#memory_size=2000,
					# output_graph=True
					)
	run_server()
	


