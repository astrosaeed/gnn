from pomdp_utils.parser import Policy,Solver
from pomdp_utils.pomdp_parser import Model
from pomdp_utils.pomdp_solver import generate_policy
import numpy as np
np.set_printoptions(precision=2)     # for better belief printing 
import random
import pathlib
import pandas as pd
import os 
import generator
from ta_env import init_tr, NUM_LOCS
from pomdp_utils.pomdp_solver import generate_policy
from graph_inference import Graph
from pgmpy.inference import BeliefPropagation, VariableElimination

class Simulator:

	def __init__(self, target, solve_pomdp=False):

		generator.Model(NUM_LOCS,'0')
		pomdp_file = pathlib.Path.cwd()/'pomdp_utils/model.pomdp'
		assert pathlib.Path(pomdp_file).is_file(), 'POMDP path does not exist'

		solver_path = '/home/saeid/software/sarsop/src/pomdpsol'
		assert pathlib.Path(solver_path).is_file(), 'Solver path does not exist'
		
		self.model = Model(pomdp_file=pomdp_file, parsing_print_flag=False)
		#################Bring line below back
		#generate_policy(solver_path, pomdp_file=pomdp_file, timeout=10)
		
		policy_file = pathlib.Path.cwd()/'pomdp_utils/model.policy'
		assert pathlib.Path(policy_file).is_file(), 'POlicy path does not exist'
		print (policy_file)
		if solve_pomdp:
			generate_policy(solver_path,pomdp_file,policy_file)		
		#assert pathlib.Path(policy_file).is_file(), 'POLICY path does not exist'

		self.policy = Policy(len(self.model.states),
							len(self.model.actions),
							policy_file=policy_file)
		

		self.target = target
		self.curr_state= np.random.choice(self.model.states[:-1])  # do not sample term
		self.curr_state_idx = self.model.states.index(self.curr_state)
		self.curr_loc = int(self.curr_state_idx/NUM_LOCS)
		self.graph = Graph(str(self.curr_loc))

	def update(self, a_idx,o_idx,b ):
		#Update belief using Bayes update 
		b = np.dot(b, self.model.trans_mat[a_idx, :])
		b = [b[i] * self.model.obs_mat[a_idx, i, o_idx] for i in range(len(self.model.states))]
		b = b / sum(b)
 
		return b


	#def pretty_print(self,b):
		#df = pd.DataFrame(b,index=False, columns=self.model.states)
		#print (df)

	def observe(self,a_idx,next_state):
		'''Make an observation using random distribution of the observation marix'''
		#s_idx = self.model.states.index(next_state)
		print ('current_loc: ', self.curr_loc)
		detected_objects = self.graph.update_curr_objs(str(self.curr_loc))
		print (detected_objects)

		if next_state =='term':
			return -1, 'na'

		if self.target not in detected_objects:
			return 1, 'Not_detected'

		print ('target obj is:')
		print (self.target)

		evidence_dic ={}
		for item in detected_objects:
			if item != self.target:
				evidence_dic[item] = 1	
				
			

		print (evidence_dic.keys())
		inf = self.infer(self.target, evidence_dic = evidence_dic)
		
		print (inf.values)
		print (type(inf.values))
		print ('line 90')
		if inf.values[0] >=0.7:
			return 0,'Detected'
		else:
			return 1, 'Not_detected'


		#return np.random.choice(self.model.observations, p= self.model.obs_mat[a_idx,s_idx,:]) 
		

	def infer(self,target, evidence_dic) :

		infer = VariableElimination(self.graph.model)
		#belief_propagation = BeliefPropagation(self.graph.model)
		print (target)
		print (evidence_dic)
	#	input()
		#inf = belief_propagation.query([target], evidence=evidence_dic)
		inf = infer.query([target], evidence=evidence_dic)
		print (inf)
		print (type(inf))
		return inf

	def run(self):

		#Initialize belief
		#b = np.ones(len(self.model.states))/(len(self.model.states)-1)
		b = np.ones(len(self.model.states))/(len(self.model.states))
		#b[-1]=0.0

		print (b)
		print (type(b))
		
		
		term=False
		
		r = 0
		ctr =0 
		#print ('shape is :', self.model.reward_mat.shape )
		while not term:
			a_idx=self.policy.select_action(b)
			assert a_idx!=-1
			print ('\n\nTimestep: ', ctr)
			s_idx = self.model.states.index(self.curr_state)		 
			r+=self.model.reward_mat[a_idx, s_idx]
			print ('Underlying state: ', self.curr_state)
			print ('action is: ',self.model.actions[a_idx])
			

			
			next_state = np.random.choice(self.model.states, p=self.model.trans_mat[a_idx,s_idx,:])
			obs_idx, obs = self.observe(a_idx,next_state)
			print ('Observation is: ', obs)
			#obs_idx = self.model.observations.index(obs)
			#print ('observation is: ',self.model.observations[obs_idx])
			print ('cost is: ',r)
			b = self.update(a_idx,obs_idx,b)
			print(b)
			print ('argmax of belief: ',np.argmax(b))
#			input()

			self.curr_state = next_state
			self.curr_state_idx = self.model.states.index(self.curr_state)
			self.curr_loc = int(self.curr_state_idx/NUM_LOCS)
			ctr+=1
			if b[-1]>0:
				term=True
				print('\n')
				print ('total reward: ',r)

def main():
	instance= Simulator('banana')
	instance.run()



if __name__ == '__main__':
	main()