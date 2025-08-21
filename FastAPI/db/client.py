from pymongo import MongoClient

db_client = MongoClient().local ### If its not defined, it connects to the default mongo instance - localhost
### Defined to local for this project