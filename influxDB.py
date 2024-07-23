import os, time
from influxdb_client_3 import InfluxDBClient3, Point, flight_client_options
import certifi
import pandas


class InfluxDB:
	token = "rFC4RChbliU6rZQp3gFqMGTx_GsNA39javQM6W7poBuoETfweyfEZNQlpfPTiPy3gAK0GX59Vku9qHqMWytnfg=="
	# token = os.environ.get("INFLUX_TOKEN")
	org = "RV"
	host = "https://us-east-1-1.aws.cloud2.influxdata.com"
	database = "Automation"
	cert = ""
	client = ""
	
	def __init__(self) -> None:
		# might not be needed for linux?
		fh = open(certifi.where(), "r")
		self.cert = fh.read()
		fh.close() 
		
	def initClient(self, database):
		# initialize client
		self.client = InfluxDBClient3(
			host=self.host, 
			token=self.token, 
			org=self.org,
			database=database,
			ssl_ca_cert=certifi.where(),
			flight_client_options=flight_client_options(
				tls_root_certs=self.cert)
			)     
		
	def query(self, sql):
		self.initClient(self.database)  
		table = self.client.query(query=sql)
		print(table.to_pandas().to_json())
		
		
	def write(self, data, database=database, precision='ms'):
		# example
		# point = (
		# 	Point("table").field(column, data)
		# )
		# line code
		#     "meaurement,tag_set1,tag_set2 field_set1,field_set2 timestamp"
		#     "table,tags column1="test",column2=23.4 timestamp"

		self.initClient(database)
		self.client.write(database=database, record=data, write_precision=precision)
		

if __name__ == "__main__":
	#  testing
	db = InfluxDB()

	sql = '''
		SELECT *
		FROM home
		WHERE
			time >= '2023-12-20T08:00:00Z'
			AND time <= '2023-12-20T20:00:00Z'
	'''

	db.query(sql)

# for key in data:
# 	point = (
# 		Point("census").tag("location", data[key]["location"]).field(data[key]["species"], data[key]["count"])
# 	)
# 	db.write(point)
# 	time.sleep(1) # separate points by 1 second
	


# lines = [
#     "meaurement,tag_set1,tag_set2 field_set1,field_set2 timestamp"
#     "table,tags column1="test",column2=23.4 timestamp"
#     "home,room=Living\ Room temp=21.1,hum=35.9,co=0i 1703059200",
#     "home,room=Kitchen temp=21.0,hum=35.9,co=0i 1703059200",
#     "home,room=Living\ Room temp=21.4,hum=35.9,co=0i 1703062800",
#     "home,room=Kitchen temp=23.0,hum=36.2,co=0i 1703062800",
#     "home,room=Living\ Room temp=21.8,hum=36.0,co=0i 1703066400",
#     "home,room=Kitchen temp=22.7,hum=36.1,co=0i 1703066400",
#     "home,room=Living\ Room temp=22.2,hum=36.0,co=0i 1703070000",
#     "home,room=Kitchen temp=22.4,hum=36.0,co=0i 1703070000",
#     "home,room=Living\ Room temp=22.2,hum=35.9,co=0i 1703073600",
#     "home,room=Kitchen temp=22.5,hum=36.0,co=0i 1703073600",
#     "home,room=Living\ Room temp=22.4,hum=36.0,co=0i 1703077200",
#     "home,room=Kitchen temp=22.8,hum=36.5,co=1i 1703077200",
#     "home,room=Living\ Room temp=22.3,hum=36.1,co=0i 1703080800",
#     "home,room=Kitchen temp=22.8,hum=36.3,co=1i 1703080800",
#     "home,room=Living\ Room temp=22.3,hum=36.1,co=1i 1703084400",
#     "home,room=Kitchen temp=22.7,hum=36.2,co=3i 1703084400",
#     "home,room=Living\ Room temp=22.4,hum=36.0,co=4i 1703088000",
#     "home,room=Kitchen temp=22.4,hum=36.0,co=7i 1703088000",
#     "home,room=Living\ Room temp=22.6,hum=35.9,co=5i 1703091600",
#     "home,room=Kitchen temp=22.7,hum=36.0,co=9i 1703091600",
#     "home,room=Living\ Room temp=22.8,hum=36.2,co=9i 1703095200",
#     "home,room=Kitchen temp=23.3,hum=36.9,co=18i 1703095200",
#     "home,room=Living\ Room temp=22.5,hum=36.3,co=14i 1703098800",
#     "home,room=Kitchen temp=23.1,hum=36.6,co=22i 1703098800",
#     "home,room=Living\ Room temp=22.2,hum=36.4,co=17i 1703102400",
#     "home,room=Kitchen temp=22.7,hum=36.5,co=26i 1703102400"
# ]

# sql = '''
#         SELECT *
#         FROM home
#         WHERE
#             time >= '2023-12-20T08:00:00Z'
#             AND time <= '2023-12-20T20:00:00Z'
# '''

# db = influxDB()
# # db.write(lines)
# # db.query(sql)




# data = {
# 	"point1": {
# 		"location": "Klamath",
# 		"species": "bees",
# 		"count": 23,
# 	},
# 	"point2": {
# 		"location": "Portland",
# 		"species": "ants",
# 		"count": 30,
# 	},
# 	"point3": {
# 		"location": "Klamath",
# 		"species": "bees",
# 		"count": 28,
# 	},
# 	"point4": {
# 		"location": "Portland",
# 		"species": "ants",
# 		"count": 32,
# 	},
# 	"point5": {
# 		"location": "Klamath",
# 		"species": "bees",
# 		"count": 29,
# 	},
# 	"point6": {
# 		"location": "Portland",
# 		"species": "ants",
# 		"count": 40,
# 	},
# 	}

# for key in data:
# 	point = (
# 		Point("census").tag("location", data[key]["location"]).field(data[key]["species"], data[key]["count"])
# 	)
# 	db.write(point)
# 	time.sleep(1) # separate points by 1 second

# 	print("Complete. Return to the InfluxDB UI.")