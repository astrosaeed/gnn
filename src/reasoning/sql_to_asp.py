import sys
sys.path.append("..")
import query
import subprocess
from subprocess import PIPE
import append_object_semantic_map
from collections import defaultdict
facts_file = "/home/saeidfour/catkin_ws/src/gnn/src/reasoning/facts.asp"

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


def appendtofacts(objects,grounds):


	with open(facts_file,"a+")as myfile:
		for obj in objects:
			myfile.write(obj+'\n')	
		for gr in grounds:
			
			myfile.write(gr+'\n')

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

if __name__ == '__main__':

	all_rels = query.query('near',0.1)

	for rel in all_rels:
	
		if rel[2]=='desk':
			rel[2]='table'
	#print (rel)



	all_rels = (removedups(all_rels))
	#print  (newlist)

	objects, grounds = reason_multiple(all_rels)

	#appendtofacts(objects,grounds)
	
	cmd = ["clingo", "facts.asp","rel.asp", "-n","0" ]

	process= subprocess.Popen(cmd,stdout=PIPE,stderr=PIPE)
	stdout, stderr = process.communicate()
	#print (stderr)
	#print (stdout.split('\n'))
	last =extractnear(stdout.split('\n'))


	 
	kol = list(set(last) - set(grounds))
	#print (kol)
	#append_object_semantic_map.from_sql(kol)


	######3From here, it is for the task planner
	#for each in kol:
	#	print (each)
	relstaskplan = []
	print (kol[0].split('(')[0])
	print (kol[0].split('(')[1].split(','))
	for rel in kol:
		relstaskplan.append((rel.split('(')[1].split(',')[0],rel.split('(')[0],rel.split('(')[1].split(',')[1],rel.split('(')[1].split(',')[2],rel.split('(')[1].split(',')[3]))

	print (relstaskplan)


	append_object_semantic_map.from_sql(relstaskplan)
