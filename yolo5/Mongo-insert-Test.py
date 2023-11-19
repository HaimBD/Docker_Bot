import pymongo

MONGO_URL = "mongodb+srv://{mongo_user}:{mongo_pass}@mongo.l74j5hs.mongodb.net/".format(mongo_user="Username", mongo_pass="Password")

prediction_summary = {
            'Test1': 'Test-One-One',
            'Test2': 'Test-Two-One',
            'Test3': 'Test-Third-One',
            'Test4': 'Test-Four-One',
            'Test5': 'Test-Five-One'
        }

mongo_server = pymongo.MongoClient(MONGO_URL)
mongo_database = mongo_server["docker"]
mongo_collection = mongo_database["Data"]
mongo_collection.insert_one(prediction_summary)
