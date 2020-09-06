import numpy as np
from ta_env import init_tr, NUM_LOCS
from pathlib import Path
import pandas as pd
parent_folder = Path('/home/saeid/gnn/data')
current_folder = parent_folder/'ta_area/front/rels/'

def read_csv(filename):
	#global relation_dict
	
	df = pd.read_csv(filename,delimiter='\t')
	#print (df.head())
	df['obj1_x_mean'] = df[['obj1_1','obj1_3']].mean(axis=1).astype('int').astype('str')
	df['obj1_y_mean'] = df[['obj1_2','obj1_4']].mean(axis=1).astype('int').astype('str')
	df['obj2_x_mean'] = df[['obj2_1','obj2_3']].mean(axis=1).astype('int').astype('str')
	df['obj2_y_mean'] = df[['obj2_2','obj2_4']].mean(axis=1).astype('int').astype('str')

	df= df[df['prob']>0.1]
	df = df[df.obj2 != "house" ]
	df = df[df.obj2 != "room"]
	df = df[df.obj2 != "leg"]
	df = df[df.obj1 != "leg"]
	df = df[df.obj1 != "window"]
	df = df[df.obj2 != "window"]
	df = df[df.obj1 != "tile"]
	df = df[df.obj2 != "tile"]

	return df.head(6)

class Model(object):
	def __init__(self, num_locs, num_objs):

		self.create_states(num_locs, num_objs) 
		self.create_actions(num_locs)
		'''
		A mistake to learn: I was trying to append to an inline list
		and Python was returning None to me 
		'''

		self.tr_func = self.create_transitions(num_locs, num_objs)

		#self.observations=['human','bag','laptop','table']
		self.observations=['human','bag']
		assert len(self.observations) == num_objs
		self.target_obj = 'human'
		self.rew_mat = self.create_reward_func(num_locs,num_objs)

	def create_states(self,num_locs, num_objs):
		states=[]
		for i in range(num_locs):
			for j in range(num_objs):
				states.append('l'+str(i)+'r'+str(j))
	
		states.append('term')
		self.states= states

	def create_actions(self,num_locs):
		self.actions=  ['go_l'+str(i) for i in range(num_locs)]
		self.actions.append('terminate')
		print (self.actions)

	def create_transitions(self, num_locs, num_objs):
		tr_func = np.zeros([len(self.actions),len(self.states),len(self.states)])   # ahrd-coded for now
#	def spat_to_act():
		tr_four_directions = init_tr()
		#print (tr_four_directions)
		print (tr_four_directions[:,0,:])

		for j in range(num_locs): # init state
			for k in range(num_locs): # resulting state
				#print (tr_four_directions[0,k,j])
				if tr_four_directions[0,j,k]==1 or tr_four_directions[1,j,k]==1 or tr_four_directions[2,j,k]==1 or tr_four_directions[3,j,k]==1:
					# avoided the loop below
					tr_func[k,j*num_objs:j*(num_objs+1),k*num_objs:k*(num_objs+1)] = 1.0 
					#for i in range(num_objs): 
					#	tr_func[k,j*num_objs+i,k*num_objs+i] = 1.0

		#print (tr_func[0,:,:])					
		return tr_func


	def create_obs_func(self):
		pass

	def create_reward_func(self, num_locs,num_objs):
		rew = np.zeros([len(self.actions),len(self.states)])
		rew[:-1,:] = -5.0  # non-terminal actions
		targ_idx = self.observations.index(self.target_obj)
		rew[-1,:] =-100
		for i in range(num_locs):
			print (i*num_objs+targ_idx)
			rew[-1,i*num_objs+targ_idx]=100
		#print (rew[-1])
		return rew
	def read_all_rels(self):
		all_csvs= [e for e in sorted((current_folder).iterdir())]
		dfs=[read_csv(x) for x in all_csvs]
		print (dfs[0])
		s = pd.Series(dfs[0]['obj1'])
		
		print (s)

	def generate(self):
		with open('model.pomdp','w+') as f:

			f.write('discount:0.99\nvalues:reward\nstates: ')
			for state in self.states:
				f.write(state+' ')
			f.write('\nactions: ')
			for action in self.actions:
				f.write(action+' ')
			f.write('\nobservations: ')
			for obs in self.observations:
				f.write(obs+' ')
			f.write('\nstart: uniform')
			#f.write('\nTransitions: ')
			for i,action in enumerate(self.actions):
				f.write('\nT:'+action+'\n')
				for j in range(len(self.states)):
					for k in range(len(self.states)):
						f.write(str(self.tr_func[i,j,k])+' ')
					f.write('\n')
			# reward function
			print (self.actions)
			for i,action in enumerate(self.actions[:-1]):
				f.write('\nR: '+action+' : * : * : * ' + str(self.rew_mat[i,0])) #because all actions have same cost
			for i,state in enumerate(self.states):
				f.write('\nR: terminate'+' : '+state+' : * : * ' + str(self.rew_mat[len(self.actions)-1, i])) #because all actions have same cost
				
			
		print ('\nDone with generating files')
def main():

	a = Model(10, 2)
	#a.create_states(3,4)
	#print (a.actions)
	a.generate()



if __name__ == '__main__':
	main()
