import pymongo
from pymongo import MongoClient
import json
from bson import ObjectId, json_util
from bson.json_util import dumps
from flask import Flask, render_template, jsonify , Response, request
from dotenv import load_dotenv
import os
from .connection import *
from math import radians, cos, sin, asin, sqrt
from collections import OrderedDict

@app.route('/signup', methods =['POST' ])
def signup () :
   #data = db.storeOwner
   
   req_Json= request.json
   email=req_Json['email']
   password=req_Json['password']
   storeName=req_Json['storeName']

   Filter = {"email":email}
   if db.storeOwner.count_documents(Filter):
     return("This email already has an store. Try another one.")
   else:
     db.storeOwner.insert_one({"email": email, "password": password, "storeName": storeName, "contacts":{"phone_number":"", "facebook_link":"", "another_link":"" }, "image":"", "long":0.0, "lat":0.0})
     result = db.storeOwner.find_one({'email': email},{'_id':1})
     print(result)
     return json.dumps(result, indent=4, default = json_util.default)
  
###########################################################################################
@app.route('/login', methods = ['POST'])
def login():
    data = db.storeOwner
    req_Json= request.json
    email=req_Json['email']
    password=req_Json['password']
    result = data.find_one({'email':email , 'password':password},{"email":0 , "password":0})
    print(result)
    
    return json.dumps(result, indent=4, default = json_util.default)

###########################################################################################
@app.route('/edit_profile', methods =['Put'])
def editProfile () :

  req_Json= request.json
  ID=req_Json['ID']
  storeName=req_Json['storeName']
  phone_number=req_Json['phone_number']
  facebook_link=req_Json['facebook_link']
  another_link=req_Json['another_link']
  image=req_Json['image']
  long=req_Json['long']
  lat=req_Json['lat']

  data = db.storeOwner.update_one({"_id":ObjectId(ID)}, 
   {   "$set": {"storeName":storeName, "contacts":{"phone_number":phone_number, "facebook_link":facebook_link, "another_link":another_link },'image':image, 'long':long, 'lat':lat}   } )

  return 'Profile updated successfully.'

###########################################################################################
@app.route('/delete_account', methods = ['DELETE'])
def deleteAccount():
    req_Json= request.json
    ID=req_Json['ID']
    data = db.storeOwner.delete_one({'_id':ObjectId(ID)})

    return 'Account deleted successfully'
###########################################################################################

@app.route('/searchStore/<store_name>', methods = ['GET'])
def search_store(store_name):
  list=[]
  #req_Json= request.json
  #store_name=req_Json['store_name']

  regex = ".*" + store_name + ".*"

  for result in db.storeOwner.find( {"storeName" : {'$regex' : regex, "$options":"i"}},{"storeName":1, "image":1} ):
      list.append(result)
  print(list)
  return json.dumps(list, indent=4, default = json_util.default)
###########################################################################################

@app.route('/storeDetail/<ID>', methods = ['GET'])
def view_store(ID):
   # list=[]
    data = db.storeOwner
    #req_Json= request.json
    #ID=req_Json['ID']
    result = data.find_one({'_id':ObjectId(ID)},{"email":0, "password":0})
    print(result)

    """for result in db.product.find({"store_id":ObjectId(ID)},{"store_id":0}):
      #list.append(result1)
      print(result)"""
    return json.dumps( (result) , indent=4, default=json_util.default)
###########################################################################################

@app.route('/getAllStores', methods = ['GET'])
def view_all_stores():
    list=[]
    data = db.storeOwner

    
    for result in data.find({},{ '_id':1 , 'storeName':1, 'image':1}):
      list.append(result)
    print(list)
    return json.dumps(list, indent=4, default=json_util.default)
###########################################################################################




list0=[]
def dist(  long1, lat1 , long2, lat2):
      dlon= long2 - long1
      dlat= lat2 - lat1
      a= sin(dlat/2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
      c= 2 * asin(sqrt(a))
      km= 6371 * c
     # print (type(long2))
      return(km) 

      
@app.route('/location', methods = ['POST'])
def loc():
    
    
    data = db.storeOwner
    product_data = db.product
    req_Json= request.json
    name=req_Json['name']
    long1=req_Json['long1']
    lat1=req_Json['lat1']
    
    ids=[]
    loc=[]
    dic={}
    for result in product_data.find({'name':name },{'_id':0, 'store_id':1}):
      idd=result["store_id"]
      idd= str(idd)
      ids.append(idd)
    for item in ids:
      for result in data.find({'_id':ObjectId(item) },{'_id':0, 'long':1, 'lat':1, 'storeName':1}):
        loc.append(result)
        long=result['long']
        lat =result['lat']
        storeName=result['storeName']
        f=dist (long1, lat1, long, lat ) 
        dic[f]=storeName
    dic = OrderedDict(sorted(dic.items()))
    final_result= list(dic.values())[:6]
    print(final_result)
      
    return json.dumps(final_result, indent=4, default=json_util.default)
