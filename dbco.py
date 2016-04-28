from pymongo import MongoClient, errors

CRAWLER_DBNAME = 'hgp_crawler'
WEBAPP_DBNAME = 'hgp_webapp'

# TODO: Move this to a config file.
localConnection = 'mongodb://127.0.0.1:27017/'
client = MongoClient(localConnection)
db = client[CRAWLER_DBNAME]
webapp_db = client[WEBAPP_DBNAME]
