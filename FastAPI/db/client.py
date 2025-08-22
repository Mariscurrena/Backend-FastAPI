from pymongo import MongoClient

### Defined to local for this project
# db_client = MongoClient().local ### If its not defined, it connects to the default mongo instance - localhost

### Connection to Mongo Atlas
db_client = MongoClient("mongodb+srv://test:test@cluster0.x3uazpo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").test