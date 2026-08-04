from pymongo import MongoClient

uri = "mongodb+srv://nayakamrutansu190_db_user:NJW1ERQJV4SfSl2v@cluster0.clgzhdk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)

try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)