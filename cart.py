import os
from flask import Flask, jsonify, request
import requests
from flask_sqlalchemy import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'cart.sqlite')
# db = SQLAlchemy(app)

cart = [
    {"user_id" : 1, "items" : {}, "total_price" : 0.0} , 
    {"user_id" : 2, "items" : {}, "total_price" : 0.0},
    {"user_id" : 3, "items" : {}, "total_price" : 0.0},
]

@app.route('cart/<int:user_id>', methods=['GET'])
def get_cart_info(user_id):
       for item in cart:
        if cart['id'] == user_id:
            return jsonify({"User info": cart}), 200
        else:
            return jsonify({"Error": "User not found"}), 404
        
@app.route('cart/<int:user_id>/add/<int:product_id>', methods=['POST'])  
def add_to_cart(user_id,product_id):
     if 'quantity' in request.json:
        decrease_quant = request.json['quantity']
     else:
         return jsonify({"Error": "Quantity not specified"}), 404   
    # Does the user exist 
     if user_id not in cart:
        return jsonify({"Error": "User not found"}), 404 
     if decrease_quant < 0:
        return jsonify({"Error": "Has to be a postive number"}), 404
    
    # Does the product exist 
     response = requests.get(f'https://product-3q2q.onrender.com/products/{product_id}')
     
     if response.status_code() == 404:
         return jsonify({"Error": "Product not found"})

    # adding the product to cart 
     response1 = requests.post(f'https://product-3q2q.onrender.com/products/{product_id}',json={'quantity' : decrease_quant, "user_id" : user_id})
     
     if response1.status_code == 200:
          return jsonify({"message": "Product addded to cart"})
     else:
        return jsonify({"Error": "Can not add product to cart"})
     
       
@app.route('/cart/<int:user_id>/remove/<int:product_id>',methods=['POST'])
def remove_from_cart(user_id,product_id):
     if 'quantity' in request.json:
        decrease_quant = request.json['quantity']
     else:
         return jsonify({"Error": "Quantity not specified"}), 404   
    # Does the user exist 
     if user_id not in cart:
        return jsonify({"Error": "User not found"}), 404 
     if decrease_quant > 0:
        return jsonify({"Error": "Has to be a negative number"}), 404
    
    # Does the product exist 
     response = requests.get(f'https://product-3q2q.onrender.com/products/{product_id}')
     
     if response.status_code() == 404:
         return jsonify({"Error": "Product not found"})

    # adding the product to cart 
     response1 = requests.post(f'https://product-3q2q.onrender.com/products/{product_id}',json={'quantity' : decrease_quant, "user_id" : user_id})
     
     if response1.status_code == 200:
          return jsonify({"message": "Product addded to cart"})
     else:
        return jsonify({"Error": "Can not add product to cart"})
    
    
    
   

if __name__ == '__main__':
    app.run(debug=True,port=5001)
      

