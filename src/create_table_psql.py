import psycopg2
import config
import argparse

def create_main_table(tablename):
	""" create tables in the PostgreSQL database"""
	commands = (
		"""
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
			r FLOAT(2)
		)
		""",
		""" CREATE TABLE dummy1 (
				part_id SERIAL PRIMARY KEY
				)
		"""
			)
	conn = None
	try:
	  
		# connect to the PostgreSQL server
		
		conn = psycopg2.connect("dbname="+config.dbname+" user="+config.user+" host="+config.host+" password="+config.password)
		print ('connected')


		cur = conn.cursor()
		# create table one by one
		
		for command in commands:
			print (command)
			cur.execute(command)

		print ('executed')
		# close communication with the PostgreSQL database server
		cur.close()
		# commit the changes
		conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)

	finally:
		if conn is not None:
			conn.close()
			print ('Hooray')

def create_meta_table(tablename):
	""" create tables in the PostgreSQL database"""
	commands = (
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
		""",
		""" CREATE TABLE dummy2 (
				part_id SERIAL PRIMARY KEY
				)
		"""
			)
	conn = None
	try:
	  
		# connect to the PostgreSQL server
		
		conn = psycopg2.connect("dbname="+config.dbname+" user="+config.user+" host="+config.host+" password="+config.password)
		print ('connected')


		cur = conn.cursor()
		# create table one by one
		
		for command in commands:
			print (command)
			cur.execute(command)

		print ('executed')
		# close communication with the PostgreSQL database server
		cur.close()
		# commit the changes
		conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)

	finally:
		if conn is not None:
			conn.close()
			print ('Hooray')



if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--maintable', type=str, required=True,
						help="main table name")
	parser.add_argument('--metatable', type=str, required=True,
						help="mets table name")
	args = parser.parse_args()
	for k, v in vars(args).items():
		globals()['FLAGS_%s' % k] = v

	create_main_table(FLAGS_maintable)
	create_meta_table(FLAGS_metatable)
