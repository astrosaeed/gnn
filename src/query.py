
import psycopg2 as pg
import csv
import config
import argparse
import glob

def query(predtype,prob):
	if predtype == 'high':
	
		sql_select = """SELECT DISTINCT filename,obj1,predicate,obj2 FROM """+config.maintable +"""
		WHERE prob>"""+str(prob)+""" AND id<6 AND obj2!='train' AND obj1!='tile' AND obj2 !='plane'"""

	elif predtype == 'near':
	
		sql_select = """SELECT DISTINCT obj1,predicate,obj2,x,y,r,filename FROM """+config.maintable +"""
		WHERE prob>"""+str(prob)+""" AND id<15 AND obj2!='bed' AND predicate='near' """

	elif predtype == 'human':
	
		sql_select = """SELECT DISTINCT filename,obj1,predicate,obj2,x,y,r FROM """+config.maintable +"""
		WHERE prob>"""+str(prob)+""" AND id<4 AND (obj1='man' OR obj1='woman'  )"""

	conn = None
	try:
		conn = pg.connect("dbname="+config.dbname+" user="+config.user+" host="+config.host+" password="+config.password)
		print ('connected')
		cursor = conn.cursor()
	
		cursor.execute(sql_select)
		all_rels = cursor.fetchall()
		print (len(all_rels))
		#print (all_rels)
		results= [list(r) for r in all_rels]
		conn.commit()
		print ('Done') 
	except (Exception, pg.Error) as e:
		print(e)
		return False
	finally:
		if (conn):
			cursor.close()
			conn.close()
			print("Connection closed.")
			return results



if __name__ == '__main__':

	#query('near',0.1)
	query('human',0.4)
