from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
import yaml

def intializeConnector():

    with open("configDb.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    admin = cfg['mysql']['user']
    pwd = cfg['mysql']['password']
    host = cfg['mysql']['host']
    DB = cfg['mysql']['db']

    mongoCred = "mongodb+srv://" + admin + ":" + pwd + "@"+ host + "?retryWrites=true"


    client = MongoClient(mongoCred)
    # list database
    print(client.list_database_names())
    db = client[DB]

    # Issue the serverStatus command and print the results
    # serverStatusResult=db.command("serverStatus")
    # pprint(serverStatusResult)

    return db

