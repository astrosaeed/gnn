
import psycopg2 as pg
import csv
import config
import argparse
import glob

def updatemaintable(maintable,metatable):

	
	sql_update = """UPDATE """+maintable+"""
	SET x="""+metatable+""".x2, y="""+metatable+""".y2
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

	updatemaintable(config.maintable,config.metatable)
