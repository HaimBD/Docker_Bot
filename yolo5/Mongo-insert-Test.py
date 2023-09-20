import pymongo

prediction_summary = {
            'Test1': 'Test-One',
            'Test2': 'Test-Two',
            'Test3': 'Test-Third',
            'Test4': 'Test-Four',
            'Test5': 'Test-Five'
        }

mongo_server = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_database = mongo_server["docker"]
mongo_collection = mongo_database["Data"]
mongo_collection.insert_one(prediction_summary)