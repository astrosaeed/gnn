import copy
from math import sqrt , pow
from pprint import pprint
import sys
sys.path.append("..")
import query
import subprocess
from subprocess import PIPE
import append_object_semantic_map
from collections import defaultdict
facts_file = "/home/saeidfour/catkin_ws/src/gnn/src/reasoning/facts.asp"

def eucdist(p1, p2):
	return sqrt(pow(p1[0]-p1[1],2)+pow(p2[0]-p2[1],2))	

def removedups(givenlist):
	finallist=[]
	withoutid =[]
	for num in givenlist:
		if num not in finallist and None not in num and num[:-1] not in withoutid:
			finallist.append(num)
			withoutid.append(num[:-1])
	return finallist

def refineasp(givenlist):
	same=[]
	
	for i in range(len(givenlist)):
		for j in range(i,len(givenlist)):
			if givenlist[i][0] == givenlist[j][2] and givenlist[i][2] == givenlist[j][0] and givenlist[i][1] == givenlist[j][1] and givenlist[i][3:-1] == givenlist[j][3:-1]:
				print ('hi')
				same.append(givenlist[j])
			
	return  list(set(givenlist) -set(same))



def extractnear(givenlist):
	finallist=[]
	
	for num in givenlist:
		if 'near'  in num:
			rels= num.split(' ')
			for rel in rels:
				if 'near' in rel:

					finallist.append(rel)

	return finallist


def appendtofacts(objects,groundsdict):


	with open(facts_file,"a+")as myfile:
		for obj in objects:
			myfile.write('object('+obj+').\n')	
		for grkey in groundsdict.keys():
			
			aspfact = grkey[0]+'('+grkey[1]+','+grkey[2]+','+grounds[grkey][0][0]+').'

			myfile.write(aspfact+'\n')

	print ('Done with facts')




def reason_multiple(all_rels):
	grounds =[]
	objects= []
	objdict= defaultdict(int)
	reldict = defaultdict(int)
	for rel in all_rels:
		#objdict
		#print (rel)
		objects.append('object('+rel[0]+').')
		objects.append('object('+rel[2]+').')
		grounds.append(rel[1]+'('+rel[0]+','+rel[2]+','+str(int(rel[3]))+','+str(int(rel[4]))+','+str(int(rel[6]))+').')
#	print (objects)
#	print (grounds)


	return objects, grounds

def sql_to_asp_human():

	all_rels = query.query('human',0.4)
	all_rels = (removedups(all_rels))
	#print  (all_rels)

	preddicts=defaultdict(list)
	framedicts=defaultdict(list)

	for record in all_rels:
		rel = (record[1],record[0],record[2])
		coord = (record[3],record[4])
		frame_id = record[5]


		if len(preddicts[rel])==0:
			print ('added')
			preddicts[rel].append((frame_id,coord))
			print (type(frame_id))
			framedicts[frame_id].append(coord)
		else:
			temp = copy.deepcopy(preddicts[rel])
			for anypoint in temp:
	#			print (anypoint)
	#			print eucdist(coord, anypoint[1])
				if eucdist(coord, anypoint[1]) <2:
					print('hi')
				else:
					preddicts[rel].append((frame_id,coord))
					framedicts[frame_id].append(coord)

	print ('before')
	pprint (preddicts)

	append_object_semantic_map.from_sql(preddicts)



	
def sql_to_asp_spatial():

	all_rels = query.query('near',0.1)

	for rel in all_rels:
	
		if rel[2]=='desk':
			rel[2]='table'
	#print (rel)



	all_rels = (removedups(all_rels))
	#print  (all_rels)

	preddicts=defaultdict(list)
	framedicts=defaultdict(list)
	objects = []
	for record in all_rels:
		rel = (record[1],record[0],record[2])
		coord = (record[3],record[4])
		frame_id = record[5]
		if record[0] not in objects:
			objects.append(record[0])
		if record[2] not in objects:

			objects.append(record[2])

		if len(preddicts[rel])==0:
			print ('added')
			preddicts[rel].append((frame_id,coord))
			print (type(frame_id))
			framedicts[frame_id].append(coord)
		else:
			temp = copy.deepcopy(preddicts[rel])
			for anypoint in temp:
	#			print (anypoint)
	#			print eucdist(coord, anypoint[1])
				if eucdist(coord, anypoint[1]) <2:
					print('hi')
				else:
					preddicts[rel].append((frame_id,coord))
					framedicts[frame_id].append(coord)

	print ('before')
	pprint (len(preddicts.keys()))
	
	
	#objects, grounds = reason_multiple(all_rels)
	grounds = preddicts
	#appendtofacts(objects,grounds)
	
	cmd = ["clingo", "facts.asp","rel.asp", "-n","0" ]
	
	process= subprocess.Popen(cmd,stdout=PIPE,stderr=PIPE)
	stdout, stderr = process.communicate()
	
	last =extractnear(stdout.split('\n'))
	for each in last:
		splitted = (each.split(','))
		#print (splitted)
		rel = (splitted[0].split('(')[0],splitted[0].split('(')[1],splitted[1])
		
		fr_id = splitted[2].split(')')[0]
		

		#print (framedicts[fr_id[:-1]])
		if rel not in preddicts.keys():
			preddicts[rel].append((fr_id,framedicts[fr_id][0]))

	print ('after')
	pprint (preddicts)
	

	append_object_semantic_map.from_sql(preddicts)


	

if __name__ == '__main__':


	sql_to_asp_human()


	