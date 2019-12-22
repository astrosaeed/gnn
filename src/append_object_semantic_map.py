import pandas as pd

#image_info_path=

object_name = 'logo'
object_x = '-36.4'
object_y = '-32.35'


semantic_path = "/home/saeidfour/catkin_ws/src/bwi_common/utexas_gdc/maps/real/3/objects.yaml"
facts_path = "/home/saeidfour/catkin_ws/src/bwi_common/bwi_kr_execution/domain_kinetic/navigation_facts.asp"

#with open(semantic_path,"a+")as myfile:
#	myfile.write("- name: "+object_name+'\n  point: ['+object_x+', '+object_y+', 0.0]')

with open(facts_path,"a+")as myfile:
	print ('hi')
	myfile.write('object('+object_name+').\ninside('+object_name+','+'main_corr'+').')
print ('Done')
