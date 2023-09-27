import os
from flask import Flask, jsonify, request
import requests
from flask_sqlalchemy import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'cart.sqlite')
# db = SQLAlchemy(app)

cart = [
    {"user_id" : 1, "items" : {5 : {"quantity" : 1, "total_price" : 3.0} }} , 
    {"user_id" : 2, "items" : {2: {"quantity" : 1, "total_price" : 1.50}}},
    {"user_id" : 3, "items" : {1: {"quantity" : 1, "total_price" : 1.99}}}
]

@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart_info(user_id):
    for item in cart:
        if item['user_id'] == user_id:
            return jsonify({"User info": item}), 200    
    return jsonify({"Error": "User not found"}), 404
        
@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])  
def add_to_cart(user_id,product_id):
     if "quantity" in request.json:
        quant = request.json["quantity"]
     else:
         return jsonify({"Error": "Quantity not specified"}), 400 
     user_exisit = False
    # Does the user exist 
     for user in cart:
        if user["user_id"] == user_id:
            user_exisit = True 
            break
        
     if user_exisit == False:
         return jsonify({"Error": "User not found"}), 404 
        
     if quant < 0:
        return jsonify({"Error": "Has to be a postive number"}), 400
    
    # Does the product exist 
     response = requests.get(f'https://product-cn9q.onrender.com/products/{product_id}')
     product = response.json()["products"]
     
     
     if response.status_code == 404:
         return jsonify({"Error": "Product not found"})

    # adding the product to cart 
     response1 = requests.post(f'https://product-cn9q.onrender.com/products/{product_id}',json={'quantity' : quant})
     if response1.status_code == 200:
          if product_id in cart[user_id - 1]['items']:
              cart[user_id-1]['items'][product_id]['quantity'] += quant
              cart[user_id-1]['items'][product_id]['total_price'] +=  quant * product['price']  
          else:
                cart[user_id-1]['items'][product_id] = {
                    "quantity" : quant,
                    "total_price" : quant * product["price"]
                }    
         
     return jsonify({"message": "Product addded to cart" })

     
       
@app.route('/cart/<int:user_id>/remove/<int:product_id>',methods=['POST'])
def remove_from_cart(user_id,product_id):
    if "quantity" in request.json:
        quant = request.json["quantity"]
    else:
         return jsonify({"Error": "Quantity not specified"}), 400 
     
    user_exisit = False
    # Does the user exist 
    for user in cart:
        if user["user_id"] == user_id:
            user_exisit = True 
            break
        
    if user_exisit == False:
         return jsonify({"Error": "User not found"}), 404 
        
    if quant > 0:
        return jsonify({"Error": "Has to be a negative number"}), 400
    
    # Does the product exist 
    response = requests.get(f'https://product-cn9q.onrender.com/products/{product_id}')
    product = response.json()["products"]
      
    if response.status_code == 404:
         return jsonify({"Error": "Product not found"})

# adding the product to cart 
    response1 = requests.post(f'https://product-cn9q.onrender.com/products/{product_id}',json={'quantity' : quant})
    if response1.status_code == 200:
        if product_id in cart[user_id - 1]['items']:
            cart[user_id-1]['items'][product_id]['quantity'] += quant
            cart[user_id-1]['items'][product_id]['total_price'] +=  quant * product['price']    
        
    return jsonify({"message": "Product removed from to cart", "User cart" : cart[user_id - 1] })
     
    
    
    
   

if __name__ == '__main__':

    app.run(debug=True,port=5001)
      

