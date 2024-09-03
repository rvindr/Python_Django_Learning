from pymongo.mongo_client import MongoClient

# create a new client and connect to the server
client = MongoClient('mongodb://localhost:27017/')

try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connect to MongoDb!")

except Exception as e:
    print(e)

db = client.expense
expense_coll = db.expenses