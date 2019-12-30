import sys
sys.path.append("..")
import query
import subprocess
from subprocess import PIPE

facts_file = "/home/saeidfour/catkin_ws/src/gnn/src/reasoning/facts.asp"

def removedups(givenlist):
	finallist=[]
	withoutid =[]
	for num in givenlist:
		if num not in finallist and None not in num and num[:-1] not in withoutid:
			finallist.append(num)
			withoutid.append(num[:-1])
	return finallist

def extractnear(givenlist):
	finallist=[]
	
	for num in givenlist:
		if 'near'  in num:
			rels= num.split(' ')
			for rel in rels:
				if 'near' in rel:

					finallist.append(rel)

	return finallist


def appendcsv(objects,grounds):


	with open(facts_file,"a+")as myfile:
		for obj in objects:
			myfile.write(obj+'\n')	
		for gr in grounds:
			
			myfile.write(gr+'\n')

	print ('Done with facts')


all_rels = query.query('near',0.1)
for rel in all_rels:
	
	if rel[2]=='desk':
		rel[2]='table'
	#print (rel)



newlist = (removedups(all_rels))
#print  (newlist)

def reason_multiple(newlist):
	grounds =[]
	objects= []
	for rel in newlist:
		objects.append('object('+rel[0]+').')
		objects.append('object('+rel[2]+').')
		grounds.append(rel[1]+'('+rel[0]+','+rel[2]+').')
#	print (objects)
#	print (grounds)


	return objects, grounds
init = reason_multiple(newlist)

cmd = ["clingo", "facts.asp","rel.asp", "-n","0" ]

process= subprocess.Popen(cmd,stdout=PIPE,stderr=PIPE)
stdout, stderr = process.communicate()
#print (stderr)
#print (stdout.split('\n'))
last =extractnear(stdout.split('\n'))


 
print (list(set(last) - set(init[1]))) 
