##Database parameters for connection #####
dbname="gnn"
user="postgres"
host="localhost"
password="SardarAzmun"
'''
For each trail, I use two tables:
1- including all relations of all images
2- including the locations where each image is taken

To name the first one, I usually use the month/date as the name and 
too name the second one, I add the word 'meta' to the first table name
'''
maintable="dec28"
metatable="dec28meta"

'''
This is the folder that contains the csvfiles of all images outputs from Google Cloud
'''
resultsfolder ="./results/2019-12-28-13-21" 

'''
This is the folder that contains where each image is taken, the 2nd table in the database
uses this information to update the 2nd table
'''
metafile= "./metadata/loc_im_2019-12-28-13-21.csv"

'''
The address of the semantic map and ASP facts:
The reasoner outputs update these files
'''
import getpass
username = getpass.getuser()  # get the current linux username

semantic_path = "/home/"+username+"/catkin_ws/src/bwi_common/utexas_gdc/maps/real/3/objects.yaml" 
facts_path =  "/home/"+username+"/catkin_ws/src/bwi_common/bwi_kr_execution/domain_kinetic/navigation_facts.asp"
abs_path = '/home/'+username+'/catkin_ws/src/gnn/src/'
