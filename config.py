  ####################
 #configuration file#
####################

#Log server API url
URL = "http://127.0.0.1:8000/get/log/"

#SQL config
HOST = "localhost"
USER = "amit"
PASSWORD = "pass"
DB_NAME = "testdb"
TABLE_RESPONSE = "API_PERFORM"
TABLE_STATUS = "API_STATUS"

#Redis server
REDIS_SERVER = "localhost"
REDIS_PORT = 6379
REDIS_HNAME = "APIHASH"

#Time Period between which api logs are queried from MySQLDB
T1 = "2015-8-5 13:28"
T2 = "2015-8-5 13:38"

#HTTP status codes
STATUS = ['200', '302', '403', '404', '409', '500', '400']
