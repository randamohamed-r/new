import pymongo
from pymongo import MongoClient
import json
from bson import ObjectId, json_util
from bson.json_util import dumps
from flask import Flask, render_template, jsonify , Response, request
from dotenv import load_dotenv
import os
from .connection import *
from translate import Translator
translator= Translator(to_lang="ar")



##Testing  


@app.route('/')
def index():
    # A welcome message to test our server
    return "<h1>Welcome to our medium-greeting-api!</h1>"

    
@app.route('/hello', methods = ['GET'])
def DisplayHelloworld():
  return jsonify({"message":"Hello"})

#################     Plants     ################
@app.route('/getAllPlants', methods = ['GET'])
def viewAllPlants():
    list=[]
    data = db.plants

    for result in data.find({},{ '_id':1 , 'name':1, 'image':1, 'sub_overview':1}):
      list.append(result)
    print(list)
    return json.dumps(list, indent=4, default=json_util.default)
##########################################################################################

@app.route('/plantById', methods = ['GET'])
def viewPlant():
    data = db.plants
    result_list=[]
    translated_list=[]
    req_Json= request.json
    ID=req_Json['ID']
    lang=req_Json['lang']
    
    result = data.find_one({'_id':ObjectId(ID)},{'_id':0, "sub_overview": 0})
    if lang=='eng':
      print(result)
      return json.dumps(result, indent=4, default=json_util.default)
    elif lang=='arab':
      result_list=list(result.values())
      for i in result_list:
        if result_list.index(i)==0 : translated_list.append(i) 
        else:
          translation = translator.translate(i)
          translated_list.append(translation)
      #list0.append(translated_list)
    print(translated_list)
    return json.dumps(translated_list, indent=4, default=json_util.default)
##########################################################################################

@app.route('/search', methods = ['GET'])
def search_plant():
  list=[]
  req_Json= request.json
  plant_name=req_Json['plant_name']

  regex = ".*" + plant_name + ".*"

  for result in db.plants.find( {"name" : {'$regex' : regex, "$options":"i"}}, {"sub_overview": 0} ):
      list.append(result)
  print(list)
  return json.dumps(list, indent=4, default = json_util.default)
#########################################################################################