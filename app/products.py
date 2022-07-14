import pymongo
from pymongo import MongoClient
import json
from bson import ObjectId, json_util
from bson.json_util import dumps
from flask import Flask, render_template, jsonify , Response, request
from dotenv import load_dotenv
import os
from .connection import *

@app.route('/add', methods =['POST'])
def addProduct () :
   data = db.product

   req_Json= request.json
   name=req_Json['name']
   price=req_Json['price']
   image=req_Json['image']
   store_id=req_Json['store_id']
   
   Filter={"name":name, 'store_id':ObjectId(store_id)}
   if data.count_documents(Filter):
      result= "This product already exists. Try another one."
      print (result)
      
   else: 
      data.insert_one({"name":name, "price":price, "image":image, "store_id":ObjectId(store_id) })
      result = data.find_one({'name':name, 'store_id':ObjectId(store_id)},{'_id':1})
      print(result)
   return json.dumps(result, indent=4, default = json_util.default)
#########################################################################################

@app.route('/edit_product', methods =['PUT'])
def edit_product () :
   data = db.product
   req_Json= request.json
   ID=req_Json['ID']
   name=req_Json['name']
   price=req_Json['price']
   image=req_Json['image']
   
   data.update_one({"_id":ObjectId(ID)}, 
   {   "$set": {"name":name, "price":price, "image":image }  } )

   return 'Product updated successfully.'

#########################################################################################

@app.route('/delete_product', methods = ['DELETE'])
def delete_product():
    req_Json= request.json
    ID=req_Json['ID']
    data = db.product.delete_one({'_id':ObjectId(ID)})
    return 'Product deleted successfully.'

#########################################################################################

@app.route('/viewAllProducts/<ID>', methods = ['GET'])
def viewAllProducts(ID):
    list0=[]
    #req_Json= request.json
    #ID=req_Json['ID']
    data = db.product                              

    for result in data.find({"store_id":ObjectId(ID)},{"store_id":0}):
      list0.append(result)
    print(list0)
    return json.dumps(list0, indent=4, default=json_util.default)
###########################################################################################
