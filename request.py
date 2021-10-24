from pymongo import MongoClient


client = MongoClient('localhost', 27017)
collection = client.instagramParser

user = 'ryzhiknata'

for i in collection.find({'username': user,
                          'folower_username': True}):
    print(i)


user2 = 'oxana_metlinskaya'
for i in collection.find({'username': user2,
                          'folowwing_username': True}):
    print(i)

