import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["questions"]

x = mycol.delete_many({})

print(x.deleted_count, " documents deleted.")