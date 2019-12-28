
import psycopg2 as pg
import csv
import config
import argparse
import glob

def updatemaintable():

	
	sql_update = """UPDATE dec24
	SET xmap=dec24meta.x2, y=dec24meta.y2
	FROM dec24meta
	WHERE dec24.filename = dec24meta.filename"""
	conn = None
	try:
		conn = pg.connect("dbname="+config.dbname+" user="+config.user+" host="+config.host+" password="+config.password)
		print ('connected')
		cursor = conn.cursor()
	
		cursor.execute(sql_update)
		update_r = """ UPDATE dec24
						SET r=sqrt(power(xmap,2)+power(y,2))
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

	updatemaintable()
