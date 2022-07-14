import pymongo
from pymongo import MongoClient
import json
from bson import ObjectId, json_util
from bson.json_util import dumps
from flask import Flask, render_template, jsonify , Response, request
from dotenv import load_dotenv
import os
import io
from PIL import Image
from array import array
import base64
from .model_function import *
import numpy as np
from keras.models import load_model
import tensorflow as tf
import numpy as np
from keras.models import load_model
from .connection import *

@app.route('/plantDisease', methods = ['POST'])
def plantDisease():
  
  data = db.plantDisease 
  req_Json= request.json
  base64_image=req_Json['base64_image']

  model_type=req_Json['model_type']
  
  """if model_type == 'd':
    diseas()
  elif model_type == 'f':
    fruits()
  elif model_type == 'h':
    healthy()"""


  imgdata = base64.b64decode(base64_image)
  filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
  with open(filename, 'wb') as f:
    f.write(imgdata)
  
  if model_type == 'd':
    result = disease_model(filename)
    
    Filter={"disease_name":result}
    if data.count_documents(Filter):
      query = data.find_one({'disease_name':result},{})
      print (query)
    else: 
      query= "Not found."
      print (query)
  #print('Done')
  """for result in data.find({},{}):
    list.append(result)
  print(list)"""
  return json.dumps(query, indent=4, default=json_util.default)
#############################################################################

@app.route('/fruit', methods = ['POST'])
def fruit():
  
  data = db.plants
  req_Json= request.json
  base64_image=req_Json['base64_image']

  model_type=req_Json['model_type']
  
  """if model_type == 'd':
    diseas()
  elif model_type == 'f':
    fruits()
  elif model_type == 'h':
    healthy()"""


  imgdata = base64.b64decode(base64_image)
  filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
  with open(filename, 'wb') as f:
    f.write(imgdata)
  
  if model_type == 'f':
    result = fruit_model(filename)
    
    Filter={"name":result}
    if data.count_documents(Filter):
      query = data.find_one({'name':result},{})
      print (query)
    else: 
      query= "Not found."
      print (query)
  #print('Done')
  """for result in data.find({},{}):
    list.append(result)
  print(list)"""
  return json.dumps(query, indent=4, default=json_util.default)
#############################################################################

"""@app.route('/healthy', methods = ['POST'])
def healthy():
  
  data = db.plants
  req_Json= request.json
  base64_image=req_Json['base64_image']

  model_type=req_Json['model_type']
  
  


  imgdata = base64.b64decode(base64_image)
  filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
  with open(filename, 'wb') as f:
    f.write(imgdata)
  
  if model_type == 'h':
    result = healthy_model(filename)
    Filter={"name":result}
    if data.count_documents(Filter):                           
        query = data.find_one({'name':result},{})
        print (query)
    else: 
        query="Not found."
        print (query)
  #print('Done')
  
  return json.dumps(query, indent=4, default=json_util.default)"""
