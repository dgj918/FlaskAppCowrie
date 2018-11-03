from flask import Flask, render_template, flash, request
from wtforms import Form, IntegerField, TextAreaField, validators, StringField, SubmitField, DateField




class cowrieInputQuery:
    
	
    def __init__(self, startTimeStamp, endTimeStamp, numResults):
        
		db = create_engine('sqlite:///tutorial.db')
		metadata = BoundMetaData(db)
		input = Table('input', metadata, autoload=True)
		date_format = "%Y-%m-%d"
		self.startDate = datetime.strptime(startDate, '%Y-%m-%d')
		self.endDate = datetime.strptime(endDate, '%Y-%m-%d')
		self.numResults = numResults
   
    def inputQuery(self):
		start = self.startDate
		start = start.strftime('%Y-%m-%d')

		end = self.endDate
		end = end.strftime('%Y-%m-%d')
		
		num = self.numResults
            
		try:
			cnx = mysql.connector.connect(user='cowrieRemote', password='asj2381!@38089f!@$#438ash',
						  host='45.55.181.76',
						  database='cowrie')

			inputRecords = pd.read_sql_query('SELECT * FROM input WHERE timestamp BETWEEN \'%s\' AND \'%s\' LIMIT BY \'%d\'' % (start, end, num ), con=cnx)
		
		except mysql.connector.Error as err:
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					print("Something is wrong with your user name or password")
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					print("Database does not exist")
				else:
					print(err)


		return inputRecords
