import psycopg2 as pg
import csv
import config
import argparse
import glob

def create_main_table(tablename):
	""" create tables in the PostgreSQL database"""
	command = ("""
		CREATE TABLE """+tablename+""" (
			filename VARCHAR(80),
			id INT,
			obj1 VARCHAR(40) ,
			predicate VARCHAR(20) ,
			obj2 VARCHAR(40) ,
			prob FlOAT(2),
			obj1_1 FLOAT(2),
			obj1_2 FLOAT(2),
			obj1_3 FLOAT(2),
			obj1_4 FLOAT(2),
			obj2_1 FLOAT(2),
			obj2_2 FLOAT(2),
			obj2_3 FLOAT(2),
			obj2_4 FLOAT(2),
			x FLOAT(2),
			y FLOAT(2),
			r FLOAT(2))
		""")
	conn = None
#	print (type(commands))
	try:
	  
		# connect to the PostgreSQL server
		
		conn = pg.connect("dbname="+config.dbname+" user="+config.user+" host="+config.host+" password="+config.password)
		print ('connected')


		cur = conn.cursor()
		# create table one by one
				
		#for command in commands:
		#	print (command)
		cur.execute(command)

		print ('executed')
		# close communication with the PostgreSQL database server
		conn.commit()
		cur.close()
		# commit the changes
		#conn.commit()
	except (Exception, pg.DatabaseError) as error:
		print(error)

	finally:
		if conn is not None:
			conn.close()
			print ('Hooray')

def create_meta_table(tablename):
	""" create tables in the PostgreSQL database"""
	command = (
		"""
		CREATE TABLE """+ tablename+""" (
			filename VARCHAR(80),
			x1 FLOAT(2),
			y1 FLOAT(2),
			x2 FLOAT(2),
			y2 FLOAT(2),
			x3 FLOAT(2),
			y3 FLOAT(2),
			x4 FLOAT(2),
			y4 FLOAT(2)
		)
		""")
	conn = None
	try:
	  
		# connect to the PostgreSQL server
		
		conn = pg.connect("dbname="+config.dbname+" user="+config.user+" host="+config.host+" password="+config.password)
		print ('connected')


		cur = conn.cursor()
		# create table one by one
		
		#for command in commands:
		#print (command)
		cur.execute(command)

		print ('executed')
		# close communication with the PostgreSQL database server
		cur.close()
		# commit the changes
		conn.commit()
	except (Exception, pg.DatabaseError) as error:
		print(error)

	finally:
		if conn is not None:
			conn.close()
			print ('Hooray')



def append_all(parentfolder,maintable):
	allfiles = (glob.glob(parentfolder+'/*.csv'))
	print (allfiles[0])

	#file = './results/final_outputs_photo_1576700560.jpg.csv'
	sql_insert = """INSERT INTO """+maintable+""" (filename,id,obj1,predicate,
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


def append_meta(metafile,metatable):
 

	filename = metafile
	sql_insert = """INSERT INTO """+metatable+"""(filename,
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

def updatemaintable(maintable,metatable):

	
	sql_update = """UPDATE """+maintable+"""
	SET x="""+metatable+""".x1, y="""+metatable+""".y1
	FROM """+metatable+"""
	WHERE """+maintable+""".filename = """+metatable+""".filename"""
	conn = None
	try:
		conn = pg.connect("dbname="+config.dbname+" user="+config.user+" host="+config.host+" password="+config.password)
		print ('connected')
		cursor = conn.cursor()
	
		cursor.execute(sql_update)
		update_r = """ UPDATE """+maintable+"""
						SET r=sqrt(power(x,2)+power(y,2))
					"""

		cursor.execute(update_r)
		conn.commit()
		print ('Done') 
	except (Exception, pg.Error) as e:
		print(e)
	finally:
		if (conn):
			cursor.close()
			conn.close()
			print("Connection closed.")


if __name__ == '__main__':
	'''
	parser = argparse.ArgumentParser()
	parser.add_argument('--maintable', type=str, required=True,
						help="main table name")
	parser.add_argument('--metatable', type=str, required=True,
						help="mets table name")
	args = parser.parse_args()
	for k, v in vars(args).items():
		globals()['FLAGS_%s' % k] = v

	'''
	metafile = config.metafile
	resultsfolder= config.resultsfolder
	maintable=config.maintable
	metatable = config.metatable

	create_main_table(maintable)
	create_meta_table(metatable)

	#append_all(resultsfolder,maintable)
	#append_meta(metafile,metatable)

	#updatemaintable(maintable,metatable)
