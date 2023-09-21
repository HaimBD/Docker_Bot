import pymongo

prediction_summary = {
            'Test1': 'Test-One-One',
            'Test2': 'Test-Two-One',
            'Test3': 'Test-Third-One',
            'Test4': 'Test-Four-One',
            'Test5': 'Test-Five-One'
        }

mongo_server = pymongo.MongoClient("mongodb://mongo1:27017,mongo2:27017,mongo3:27017/?replicaSet=myReplicaSet")
mongo_database = mongo_server["docker"]
mongo_collection = mongo_database["Data"]
mongo_collection.insert_one(prediction_summary)