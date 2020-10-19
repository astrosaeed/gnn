
from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination, BeliefPropagation
from pathlib import Path
import pandas as pd
from collections import defaultdict
import itertools


#parent_folder = Path('/home/saeid/gnn/data')
parent_folder = Path('/home/saeid/Dropbox/gnn/data')
current_folder = parent_folder/'ta_area/front/rels/'

class Graph:

	def __init__(self):

		self.anchor_objs= ['table', 'man']
		self.men_objs = ['hand','head','chair','hat','bed']
		self.table_objs = ['laptop','banana','book','chair','paper']
		# Defining the model structure. We can define the network by just passing a list of edges.
		#print (detected)
		#model = BayesianModel([('book', 'table'), ('I', 'G'), ('G', 'L'), ('I', 'S')])
		#model = BayesianModel(detected)
		#allfiles =list((current_folder).glob('*.csv')) 
		#print (get_all_objs(allfiles))
		#input()

		#all_objs, detected =  read_csv(current_folder/'0.csv')
		#print (all_objs)

		'''bayesian_model = BayesianModel([('A', 'J'), ('R', 'J'), ('J', 'Q'),
		                                 ('J', 'L'), ('G', 'L')])
		cpd_a = TabularCPD('A', 2, [[0.2], [0.8]])
		cpd_r = TabularCPD('R', 2, [[0.4], [0.6]])
		cpd_j = TabularCPD('J', 2,
		                    [[0.9, 0.6, 0.7, 0.1],
		                     [0.1, 0.4, 0.3, 0.9]],
		                    ['R', 'A'], [2, 2])
		cpd_q = TabularCPD('Q', 2,
		                    [[0.9, 0.2],
		                     [0.1, 0.8]],
		                    ['J'], [2])
		cpd_l = TabularCPD('L', 2,
		                    [[0.9, 0.45, 0.8, 0.1],
		                     [0.1, 0.55, 0.2, 0.9]],
		                   ['G', 'J'], [2, 2])
		cpd_g = TabularCPD('G', 2, [[0.6], [0.4]])
		bayesian_model.add_cpds(cpd_a, cpd_r, cpd_j, cpd_q, cpd_l, cpd_g)
		belief_propagation = BeliefPropagation(bayesian_model)
		print (dir(belief_propagation.query(variables=['J', 'Q'],
		                          evidence={'A': 0, 'R': 0, 'G': 0, 'L': 1})))

		print (belief_propagation.query(variables=['J', 'Q'],
		                          evidence={'A': 0, 'R': 0, 'G': 0, 'L': 1}).values)
		'''




		all_arcs = itertools.product(self.anchor_objs, self.men_objs+self.table_objs)
		#all_arcs = itertools.product(anchor_objs, men_objs)
		self.model = BayesianModel(all_arcs)
		self.build_cpds()

	def read_csv(self, filename):
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
		a = df.head(6)[['obj1','obj2']].to_records(index=False)
		#a = zip(df.head(6)['obj1'], df.head(6)['obj2'])
		print (a)
		all_objs1 = set([x for (x,y) in a])
		all_objs2 = set([y for (x,y) in a])
		all_objs = all_objs1 | all_objs2
		#input()
		#normalized_prob = [x/sum(df.head(6)['prob'].to_list()) for x in df.head(6)['prob'].to_list()]
		#print (normalized_prob)
		#all_objs_dict =defaultdict(int)
		#for i,obj in enumerate(all_objs):

		#	all_objs_dict[obj]+=normalized_prob[i]
		#print (filename)
		#print (all_objs_dict)
		return all_objs ,a.tolist()

	def get_all_objs(self, allfiles):
		'''
		outputs a set of all objects in the gnn output
		'''
		temp = set()
		for each in allfiles:
			all_objs, _= self.read_csv(each)
			temp.update(all_objs)
		return temp
	
	def build_cpds(self):

		# Defining individual CPDs.
		cpds =[]
		for variable in self.anchor_objs:
			temp= TabularCPD(variable=variable, variable_card=2, values=[[0.7], [0.3]], state_names={variable: ['Detected', 'Not_detected']})
			cpds.append(temp) 

		for variable in self.men_objs:
			temp = TabularCPD(variable=variable, variable_card=2, 
		                      values=[[0.8, 0.5, 0.8,  0.5],
		                              [0.2, 0.5, 0.2, 0.5]],
		                      evidence=['table', 'man'],
		                      evidence_card=[2, 2],
		                      state_names={variable: ['Detected', 'Not_detected'],
		                                   'table': ['Detected', 'Not_detected'],
		                                   'man': ['Detected', 'Not_detected']})
			cpds.append(temp)	

		for variable in self.table_objs:
			temp = TabularCPD(variable=variable, variable_card=2, 
		                      values=[[0.8, 0.8, 0.4, 0.4],
		                              [0.2, 0.2, 0.6, 0.6]],
		                      evidence=['table', 'man'],
		                      evidence_card=[2, 2],
		                      state_names={variable: ['Detected', 'Not_detected'],
		                                   'table': ['Detected', 'Not_detected'],
		                                   'man': ['Detected', 'Not_detected']})
			cpds.append(temp)

		'''
		temp = TabularCPD(variable='table', variable_card=2, 
		                      values=[[0.5, 0.5],
		                              [0.5, 0.5]], 
		                      evidence=['man'],
		                      evidence_card=[2],
		                      state_names={'table': ['Detected', 'Not_detected'],
											'man': ['Detected', 'Not_detected']})

		cpds.append(temp)
		'''
		# The representation of CPD in pgmpy is a bit different than the CPD shown in the above picture. In pgmpy the colums
		# are the evidences and rows are the states of the variable. So the grade CPD is represented like this:
		#
		#
		#     man stuff
		# 
		#    +---------+---------+---------+---------+---------+
		#    | table   | table_d | table_d | table_n | table_n |
		#    +---------+---------+---------+---------+---------+
		#    | man     | man__d  | man__n  | man__d  | man__n  |
		#    +---------+---------+---------+---------+---------+
		#    |  obj _d | 0.8     | 0.5    | 0.8      | 0.5     |
		#    +---------+---------+---------+---------+---------+
		#    | obj_n   | 0.2     | 0.5    | 0.2      | 0.5     |
		#    +---------+---------+---------+---------+---------+


		#     table stuff
		#    +---------+---------+---------+---------+---------+
		#    | table   | table_d | table_d | table_n | table_n |
		#    +---------+---------+---------+---------+---------+
		#    | man     | man__d  | man__n  | man__d  | man__n  |
		#    +---------+---------+---------+---------+---------+
		#    |  obj _d | 0.8     | 0.8    | 0.4      | 0.4     |
		#    +---------+---------+---------+---------+---------+
		#    | obj_n   | 0.2     | 0.2    | 0.6      | 0.6     |
		#    +---------+---------+---------+---------+---------+



		# CPDs can also be defined using the state names of the variables. If the state names are not provided
		# like in the previous example, pgmpy will automatically assign names as: 0, 1, 2, ....
		'''
		cpd_g_sn = TabularCPD(variable='G', variable_card=3, 
		                      values=[[0.3, 0.05, 0.9,  0.5],
		                              [0.4, 0.25, 0.08, 0.3],
		                              [0.3, 0.7,  0.02, 0.2]],
		                      evidence=['I', 'D'],
		                      evidence_card=[2, 2],
		                      state_names={'G': ['A', 'B', 'C'],
		                                   'I': ['Dumb', 'Intelligent'],
		                                   'D': ['Easy', 'Hard']})

		cpd_l_sn = TabularCPD(variable='L', variable_card=2, 
		                      values=[[0.1, 0.4, 0.99],
		                              [0.9, 0.6, 0.01]],
		                      evidence=['G'],
		                      evidence_card=[3],
		                      state_names={'L': ['Bad', 'Good'],
		                                   'G': ['A', 'B', 'C']})

		cpd_s_sn = TabularCPD(variable='S', variable_card=2,
		                      values=[[0.95, 0.2],
		                              [0.05, 0.8]],
		                      evidence=['I'],
		                      evidence_card=[2],
		                      state_names={'S': ['Bad', 'Good'],
		                                   'I': ['Dumb', 'Intelligent']})
		'''
		# Associating the CPDs with the network

		# These defined CPDs can be added to the model. Since, the model already has CPDs associated to variables, it will
		# show warning that pmgpy is now replacing those CPDs with the new ones.
		for each in cpds:
			self.model.add_cpds(each)

		# check_model checks for the network structure and CPDs and verifies that the CPDs are correctly 
		# defined and sum to 1.
		print (self.model.check_model())

		#print (model.get_cpds())



		#print (model.check_model())

def main():

	mygraph = Graph()

	infer = VariableElimination(mygraph.model)
	belief_propagation = BeliefPropagation(mygraph.model)
	#g_dist = infer.query(['G'])

	#print(g_dist)

	#print(infer.query(['laptop'], evidence={'table': 'Detected', 'man':'Not_detected'}))
	print(infer.query(['laptop'], evidence={'table': 'Not_detected','man':'Detected','banana':'Detected'}))
	print(belief_propagation.query(['laptop'], evidence={'table': 'Not_detected',
														'man':'Detected',
														'banana':'Detected',
														'chair':'Not_detected',
														'book':'Not_detected'}))

if __name__ == '__main__':
	main()