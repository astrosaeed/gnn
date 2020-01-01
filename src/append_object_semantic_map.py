import pandas as pd
import query
import config

semantic_path = config.semantic_path
facts_path = config.facts_path

def from_sql(all_relsdict):

	with open(semantic_path,"a+")as myfile:
		for i,rel in enumerate(all_relsdict):
			print (all_relsdict[rel])
			object_name = rel[1]+'_'+rel[0]+'_'+rel[2]
			object_x = str(all_relsdict[rel][0][1][0])
			object_y = str(all_relsdict[rel][0][1][1])
			print (object_name+'\t'+str(object_x)+'\t'+str(object_y))


	
			myfile.write("\n- name: "+object_name+'\n  point: ['+object_x+', '+object_y+', 0.0]')

	with open(facts_path,"a+")as myfile:
		for rel in all_relsdict:
			
			object_name = rel[1]+'_'+rel[0]+'_'+rel[2]
			object_x = str(all_relsdict[rel][0][1][0])
			object_y = str(all_relsdict[rel][0][1][1])
			print (object_name+'\t'+str(object_x)+'\t'+str(object_y))


		
			myfile.write('\nobject('+object_name+').')


#image_info_path=
def single_image():
	object_name = 'logo'
	object_x = '-36.4'
	object_y = '-32.35'


	

	#with open(semantic_path,"a+")as myfile:
	#	myfile.write("- name: "+object_name+'\n  point: ['+object_x+', '+object_y+', 0.0]')

	with open(facts_path,"a+")as myfile:
		print ('hi')
		myfile.write('object('+object_name+').\ninside('+object_name+','+'main_corr'+').')
	print ('Done')



if __name__ == '__main__':

	all_rels =  (query.query('human',0.4))
	from_sql(all_rels)
