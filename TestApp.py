from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from bson import json_util
import json


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD']=True
app.config['SESSION_TYPE']="filesystem"
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://wwwphy2003:oXPyfh5y09Tm0qKq@cluster0.1z5x1kd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

DEBUG=True

def parse_json(data):
    return json.loads(json_util.dumps(data))

def testRestaurantsignup(email,password,area,name):
    try:
        db = client.Restaurant
        rating_data = [0,0.0,0.0]
        error_message=[]
        restaurant_data = {
            "email": email,
            "password": password,
            "area": area,
            "name": name,
            "pendingOrderId": [],
            "isRecommended": False,
            "rating": rating_data,
            "signup_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        # Insert user data into MongoDB
        collection = db['Info']
        result = collection.insert_one(restaurant_data)
    except Exception as e:
        error_message.append(str(e))

    if(len(error_message)==0):
        return "PASSED"
    else :
        if DEBUG:
            print("testRestaurantsignup")
            print(error_message)
        return "FAILED"
    
def testDeliveryAgentsignup(email,password,gender,area,mobile,dob,name):
    # Insert user data into MongoDB
    try:
        db = client.DeliveryAgent
        rating_data = [0,0.0,0.0]
        error_message=[]
        deliveryAgent_data = {
            "name" : name,
            "dob" : dob,
            "mobile" : mobile,
            "email" : email,
            "password" : password,
            "gender" : gender,
            "area" : area,
            "isAvailable" : True,
            "rating" : rating_data,
            "currentOrderId":""
        }
        collection = db['User_Info']
        result = collection.insert_one(deliveryAgent_data)
    except Exception as e:
        error_message.append(str(e))

    if(len(error_message)==0):
        return "PASSED"
    else :
        if DEBUG:
            print("testDeliveryAgentsignup")
            print(error_message)
        return "FAILED"
    
def testCustomerSignup(email,password,gender,area,mobile,dob,name,address):
    # Insert user data into MongoDB
    try:
        error_message=[]
        db = client.Customers
        rating_data = [0,0.0,0.0]
        collection = db.User_Info
        user_data = {
            "email": email,
            "password": password,
            "gender": gender,
            "area": area,
            "mobile": mobile,
            "dob": dob,
            "name": name,
            "address": address,
            "rating": rating_data,
            "pendingOrderId": [],
            "signup_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        # collection = db['User_Info']
        result = collection.insert_one(user_data)
    except Exception as e:
        error_message.append(str(e))
    
    if(len(error_message)==0):
        return "PASSED"
    else :
        if DEBUG:
            print("testCustomerSignup")
            print(error_message)
        return "FAILED"
    
# delete user from database
def testdelete_user(to_delete,user_type):
    to_delete = str(to_delete)
    try:
        error_message=[]
        if(user_type=="restaurant"):
            db = client.Restaurant
            res_str = to_delete[10:-2]

            db['Info'].delete_one({"_id": ObjectId(res_str)})
            prefix = '{"_id": "' + to_delete + '"}'
            db['foodItem'].delete_many({"restaurantId": prefix})
        elif user_type=="customer":
            db = client.Customers
            cus_str = to_delete[10:-2]
            print(cus_str)
            db['User_Info'].delete_one({"_id": ObjectId(cus_str)})
        elif user_type=="deliveryAgent":
            db = client.DeliveryAgent
            del_str = to_delete[10:-2]
            db['User_Info'].delete_one({"_id": ObjectId(del_str)})
    except Exception as e:
        error_message.append(str(e))

    if(len(error_message)==0):
        return "PASSED"
    else :
        if DEBUG:
            print("deleteUserFromDatabase")
            print(error_message)
        return "FAILED"
    
def testfoodItemAdder(name,price,restaurant_id):
    try:
        error_message=[]
        db = client.Restaurant
        foodItem = {
            "name": name,
            "pricePerItem": price,
            "isRecommended": False,
            "restaurantId": str(restaurant_id)
        }
        
        # Inserting the food item into the database for the specific restaurant
        inserted_food_item = db['foodItem'].insert_one(foodItem)    
    except Exception as e:
        error_message.append(str(e))

    if(len(error_message)==0):
        return "PASSED"
    else :
        if DEBUG:
            print("foodItemAdder")
            print(error_message)
        return "FAILED"
    
def testGetMenu(currentRestaurantMenuId):

    error_message=[]
    foodItemList=[]
    try:
        db = client.Restaurant
        food_items_collection = db['foodItem'].find({"restaurantId": currentRestaurantMenuId})
        for item in food_items_collection:
            item['_id'] = str(item['_id'])  # Convert ObjectId to string for JSON serialization
            foodItemList.append(item)
    except Exception as e:
        error_message.append(str(e))

    if(len(error_message)==0):
        return "PASSED - fetch "+str(len(foodItemList))+" items"
    else :
        if DEBUG:
            print("testGetMenu")
            print(error_message)
        return "FAILED"
    
def testGetAllRestaurant():
    restaurantList=[]
    error_message=[]
    try:
        db = client.Restaurant
        restaurant_collection = db['Info'].find({})
        for restaurant in restaurant_collection:
            restaurant['_id'] = str(restaurant['_id'])  # Convert ObjectId to string for JSON serialization
            restaurantList.append(restaurant)
    except Exception as e:
        error_message.append(str(e))

    if(len(error_message)==0):
        return "PASSED - fetch "+str(len(restaurantList))+" restaurants"
    else :
        if DEBUG:
            print("testGetAllRestaurant")
            print(error_message)
        return "FAILED"
    
def testGetAllCustomer():
    customerList=[]
    error_message=[]
    try:
        db = client.Customers
        customer_collection = db['User_Info'].find({})
        for customer in customer_collection:
            customer['_id'] = str(customer['_id'])  # Convert ObjectId to string for JSON serialization
            customerList.append(customer)
    except Exception as e:
        error_message.append(str(e))

    if(len(error_message)==0):
        return "PASSED - fetch "+str(len(customerList))+" customers"
    else :
        if DEBUG:
            print("testGetAllCustomer")
            print(error_message)
        return "FAILED"
    
def testGetAllDelivery():
    deliveryList=[]
    error_message=[]
    try:
        db = client.DeliveryAgent
        delivery_collection = db['User_Info'].find({})
        for delivery in delivery_collection:
            delivery['_id'] = str(delivery['_id'])  # Convert ObjectId to string for JSON serialization
            deliveryList.append(delivery)
    except Exception as e:
        error_message.append(str(e))

    if(len(error_message)==0):
        return "PASSED - fetch "+str(len(deliveryList))+" delivery agents"
    else :
        if DEBUG:
            print("testGetAllDelivery")
            print(error_message)
        return "FAILED"
    

def testSignIn(email,password):
    try:
        db = client.Customers
        user_data = db['User_Info'].find_one({"email": email})

        if user_data and user_data['password'] == password:
            user_data = parse_json(user_data)
            user_id = str(user_data['_id'])
            json_data = json.dumps({'_id': user_id})
    except Exception as e:
        if DEBUG:
            print("testSignIn")
            print(str(e))
        return "FAILED"
    return "PASSED"

def testchangeRecommendedFoodItem(foodItemId,restaurantId):
    try:
        error_message=[]
        restaurantId = restaurantId[9:-2]
        foodItemId = str(foodItemId)
        isRecommended=""
        db = client.Restaurant  # Replace 'your_database' with your actual database name
        food_items_collection = db['foodItem']
        foodItemId = foodItemId[10:-2]
        foodItemId = ObjectId(foodItemId)
        # Get current isRecommended value from the database
        food_item = food_items_collection.find_one({"_id": foodItemId})
        isRecommended = food_item.get('isRecommended', False)

        # Update isRecommended in the database
        food_items_collection.update_one({"_id": foodItemId}, {"$set": {"isRecommended": not isRecommended}})
        
    except Exception as e:
        error_message.append(str(e))

    if(len(error_message)==0):
        return "PASSED"
    else :
        if DEBUG:
            print("testchangeRecommendFoodItem")
            print(error_message)
        return "FAILED"
    
def testchangeRecommendedRestaurant(restaurantId):
    try:
        error_message=[]
        isRecommended=""
        db = client.Restaurant
        restaurants_collection = db['Info']
        restaurantId = restaurantId[10:-2]
        restaurantId = ObjectId(restaurantId)
        restaurant = restaurants_collection.find_one({"_id": restaurantId})
        isRecommended = restaurant.get('isRecommended', False)
    except Exception as e:
        error_message.append(str(e))
    
    try:
        restaurants_collection.update_one({"_id": restaurantId}, {"$set": {"isRecommended": not isRecommended}})
    except Exception as e:
        error_message.append(str(e))

    if(len(error_message)==0):
            return "PASSED"
    else :
        if DEBUG:
            print("testchangeRecommendedRestaurant")
            print(error_message)
        return "FAILED"

def testgetRecommendedRestaurant():
    error_message=[]
    restaurantList = []
    tempRestaurantList = []

    try:
        db = client.Restaurant
        docs = db['Info'].find()
        for doc in docs:
            doc = parse_json(doc)
            temp_dict = doc
            temp_dict['userId'] = str(doc['_id'])  
            temp_dict['areaName'] = doc['area']
            temp_dict['ratingValue'] = doc['rating'][2]
            tempRestaurantList.append(temp_dict)
    except Exception as e:
        error_message.append(str(e))  

    try:
        for restaurant in tempRestaurantList:
            if restaurant.get('isRecommended', False):
                restaurantList.append(restaurant)
    except Exception as e:
        error_message.append(str(e))

    if(len(error_message)==0):
        return "PASSED - fetch "+str(len(restaurantList))+" recommended restaurants"
    else :
        if DEBUG:
            print("testgetRecommendedRestaurant")
            print(error_message)
        return "FAILED"


################# caller functions#################

def testRestaurantsignupCaller():
    email="TestRestaurantSignup@xyz.com"
    password="passwdR"
    area="Nehru"
    name="TestingRestaurant"
    result=testRestaurantsignup(email,password,area,name)
    print("Test Restaurant Signup - "+result)

def testDeliveryAgentsignupCaller():
    email="TestDeliveryAgentSignup@xyz.com"
    password="passwdD"
    gender="Male"
    area="Nehru"
    mobile="9351238245"
    dob="29/07/1997"
    name="TestingDeliveryAgent"
    result=testDeliveryAgentsignup(email,password,gender,area,mobile,dob,name)
    print("Test Delivery Agent Signup - "+result)

def testCustomerSignupCaller():
    email="TestCustomerSignup@xyz.com"
    password="passwdC"
    gender="Male"
    area="Nehru"
    mobile="9832899562"
    dob="21/10/2006"
    name="TestingCustomer"
    address="Nehru Nagar, Ghaziabad"
    result=testCustomerSignup(email,password,gender,area,mobile,dob,name,address)
    print("Test Customer Signup - "+result)

def testDeleteUserCaller():
    user_id=""
    user_type=""
    result=testdelete_user(user_id,user_type)
    print("Test Delete User - "+result)

def testGetMenuCaller():
    currentRestaurantMenuId=""
    result=testGetMenu(currentRestaurantMenuId)
    print("Test Get Menu - "+result)

def testfoodItemAdderCaller():
    name="Burger"
    price="80"
    restaurantId=""
    result=testfoodItemAdder(name,price,restaurantId)
    print("Test Food Item Adder - "+result)

def testLoginCaller():
    email="TestCustomerSignup@xyz.com"
    password="passwdC"
    result=testSignIn(email,password)
    print("Test Signin - "+result)

def testGetAllRestaurantCaller():
    result=testGetAllRestaurant()
    print("Test Get All Restaurant - "+result)

def testGetAllCustomerCaller():
    result=testGetAllCustomer()
    print("Test Get All Customer - "+result)

def testGetAllDeliveryCaller():
    result=testGetAllDelivery()
    print("Test Get All Delivery - "+result)

def testchangeRecommendedFoodItemCaller():
    foodItemId="{'$oid': '6614106c47b3f9a6c8cceb56'}"
    restaurantId="{\"_id\": \"{'$oid': '6614105647b3f9a6c8cceb55'}\"}"
    result=testchangeRecommendedFoodItem(foodItemId,restaurantId) 
    print("Test Change Recommended FoodItem - "+result)

def testchangeRecommendedRestaurantCaller():
    restaurantId="{'$oid': '6614105647b3f9a6c8cceb55'}"
    result=testchangeRecommendedRestaurant(restaurantId)
    print("Test change Recommended Restaurant - "+result)

def testgetRecommendedRestaurantCaller():
    result=testgetRecommendedRestaurant()
    print("Test get Recommended Restaurant - "+result)

if __name__ == "__main__":
    testRestaurantsignupCaller()
    testDeliveryAgentsignupCaller()
    testCustomerSignupCaller()
    testDeleteUserCaller()  
    testGetMenuCaller()
    testfoodItemAdderCaller()
    testLoginCaller()
    testGetAllRestaurantCaller()
    testGetAllCustomerCaller()
    testGetAllDeliveryCaller()
    testchangeRecommendedFoodItemCaller()
    testchangeRecommendedRestaurantCaller()
    testgetRecommendedRestaurantCaller()
    
