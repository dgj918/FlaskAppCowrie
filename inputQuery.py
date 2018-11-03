import mysql.connector
from mysql.connector import errorcode
import datetime

class inputQuery:
    
    def __init__(self, startDate, endDate, numRecords):
        
		date_format = "%Y-%m-%d"
		self.startDate = startDate
		self.endDate = endDate
		self.numRecords = numRecords
   
    def readWindow(self):
		start = self.startDate
		end = self.endDate 
		numRecords = self.numRecords
		try:
			cnx = mysql.connector.connect(user='cowrieRemote', password='asj2381!@38089f!@$#438ash',
						  host='localhost',
						  database='cowrie')
			cursor = cnx.cursor()
			print "connection ready"

			query = ("SELECT session, timestamp, input FROM input WHERE timestamp BETWEEN %s AND %s ORDER BY timestamp LIMIT %s")
			
			cursor.execute(query, (start, end, numRecords))
			
			print "query executed"
			
			for (session, timestamp, input) in cursor:
				print("{}, {}, {}".format(session, timestamp, input))
			
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Something is wrong with your user name or password")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Database does not exist")
			else:
				print(err)
		else:
			cnx.close()


		return cursor
		


	


    









