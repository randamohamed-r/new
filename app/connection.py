import pymongo
from pymongo import MongoClient
import json
from bson import ObjectId, json_util
from bson.json_util import dumps
from flask import Flask, render_template, jsonify , Response, request
from dotenv import load_dotenv
import os



app=Flask(__name__)
load_dotenv()
password=os.getenv("DBPASSWORD") 
username=os.getenv("DBUSERNAME")
dburl=f"mongodb+srv://{username}:{password}@cluster0.v6erp.mongodb.net/?retryWrites=true&w=majority"

#print(dburl)




try:
  client = MongoClient(dburl)
  db = client.Agrosnap
  #client.server_info()
except:
  print('ERROR')