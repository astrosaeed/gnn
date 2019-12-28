import psycopg2 as pg
import csv
import config
import argparse
import glob

def append_all(parentfolder):
	allfiles = (glob.glob('./'+parentfolder+'/*.csv'))
	print (allfiles[0])

	#file = './results/final_outputs_photo_1576700560.jpg.csv'
	sql_insert = """INSERT INTO dec24(filename,id,obj1,predicate,
				obj2,prob,obj1_1,obj1_2 ,obj1_3, obj1_4,
				obj2_1 ,obj2_2 ,obj2_3 ,obj2_4 )
					VALUES(%s,%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s)"""

	conn = None
	try:
		conn = pg.connect("dbname="+config.dbname+" user="+config.user+" host="+config.host+" password="+config.password)
		print ('connected')
		cursor = conn.cursor()
		for i,file in enumerate(allfiles):
			with open(file, 'r') as f:
				print (i)
				reader = csv.reader(f)
				next(reader) # This skips the 1st row which is the header.
				for record in reader:
					#print (len(record[0].split('\t')))
					added = record[0].split('\t')
					added.insert(0,file.split('_')[-1].split('.')[0])
					cursor.execute(sql_insert, added )
					conn.commit()
	except (Exception, pg.Error) as e:
		print(e)
	finally:
		if (conn):
			cursor.close()
			conn.close()
			print("Connection closed.")


def append_meta(metafile):
 

	filename = metafile
	sql_insert = """INSERT INTO dec24meta(filename,
				x1,y1,x2,y2,x3,y3,x4,y4)
					VALUES(%s, %s, %s,%s, %s, %s, %s, %s, %s)"""

	conn = None
	try:
		conn = pg.connect("dbname="+config.dbname+" user="+config.user+" host="+config.host+" password="+config.password)
		print ('connected')
		cursor = conn.cursor()
		
		with open(filename, 'r') as f:
			print ('file read successfuly')
			reader = csv.reader(f)
			next(reader) # This skips the 1st row which is the header.
			for record in reader:
				print (len(record))
				
			  
				cursor.execute(sql_insert, record)
				conn.commit()
	except (Exception, pg.Error) as e:
		print(e)
	finally:
		if (conn):
			cursor.close()
			conn.close()
			print("Connection closed.")



if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--foldername', type=str, required=True,
						help="folder where csvfiles are stored")
	parser.add_argument('--metafile', type=str, required=True,
						help="metadata file")
	args = parser.parse_args()
	for k, v in vars(args).items():
		globals()['FLAGS_%s' % k] = v

	resultsfolder = FLAGS_foldername
	metafile = FLAGS_metafile
#	append_all(resultsfolder)
	append_meta(metafile)
