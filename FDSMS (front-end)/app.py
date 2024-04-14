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
client = MongoClient("mongodb+srv://Shshank:qLXrUo9sVzyorblA@cluster0.0edtkvu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# This is the app route for the index page
@app.route('/')
def index():
    session['signMess']="False"
    message=session['signMess']
    return render_template('index.html', message=message)


# This will render the signup page for the user
@app.route('/Signup')
def signUp():
    return render_template('signup.html')

# This will render the login page for the user
@app.route('/login')
def login():
    message=session['signMess']
    session['signMess']="False"
    return render_template('login.html', message=message)

# This will render the login page for the customer
@app.route('/customerLogin')
def customerLogin():
    message=session['signMess']
    session['signMess']="False"
    return render_template('customerLogin.html', message=message)

def parse_json(data):
    return json.loads(json_util.dumps(data))

@app.route('/login/customer', methods=['POST'])
def customerlogin():
    db = client.Customers
    email = request.form['email']
    password = request.form['password']
    print("hello")
    try:
        # Search for the user by email in the 'customers' collection
        user_data = db['User_Info'].find_one({"email": email})

        if user_data and user_data['password'] == password:
            user_data = parse_json(user_data)
            print(user_data)
            session['sessionUser'] = user_data
            session['sessionUser']['userType']="customer"
            user_id = str(user_data['_id'])
            json_data = json.dumps({'_id': user_id})
            session['userId'] = json_data
            print("hi")
            return redirect(url_for('customerDashboard'))  # Redirect to a generic dashboard
    except:
        session['signMess']="Please enter the correct credentials"
        return redirect(url_for('login')) 



# This will render the login page for the restaurant
@app.route('/restaurantLogin')
def restaurantLogin():
    message=session['signMess']
    session['signMess']="False"
    return render_template('restaurantLogin.html', message=message)

@app.route('/login/restaurant', methods=['POST'])
def restaurantlogin():
    db = client.Restaurant
    email = request.form['email']
    password = request.form['password']
    try:
        # Search for the user by email in the 'customers' collection
        user_data = db['Info'].find_one({"email": email})
        print("hello")
        if user_data and user_data['password'] == password:
            user_data = parse_json(user_data)
            session['sessionUser'] = user_data
            session['sessionUser']['userType']="restaurant"
            user_id = str(user_data['_id'])
            json_data = json.dumps({'_id': user_id})
            session['userId'] = json_data   
            print("hello")
            return redirect(url_for('restaurantDashboard'))  # Redirect to a generic dashboard
    except:
        session['signMess']="Please enter the correct credentials"
        return redirect(url_for('login')) 


# This will render the login page for the delivery agent
@app.route('/deliveryLogin')
def deliveryLogin():
    message=session['signMess']
    session['signMess']="False"
    return render_template('deliveryLogin.html', message=message)

@app.route('/login/delivery', methods=['POST'])
def deliverylogin():
    db = client.DeliveryAgent
    email = request.form['email']
    password = request.form['password']
    try:
        # Search for the user by email in the 'deliveryAgent' collection
        user_data = db['User_Info'].find_one({"email": email})
        print(user_data)
        if user_data and user_data['password'] == password:
            print(user_data)
            user_data = parse_json(user_data)
            session['sessionUser'] = user_data
            session['sessionUser']['userType']="deliveryAgent"
            user_id = str(user_data['_id'])
            json_data = json.dumps({'_id': user_id})
            session['userId'] = json_data  
            print("hello")
            return redirect(url_for('deliveryAgentDashboard'))  # Redirect to a generic dashboard
    except:
        session['signMess']="Please enter the correct credentials"
        return redirect(url_for('login')) 


# This will render the login page for the delivery agent
@app.route('/adminLogin')
def adminLogin():
    message=session['signMess']
    session['signMess']="False"
    return render_template('adminLogin.html', message=message)

@app.route('/login/admin', methods=['POST'])
def adminlogin():
    db = client.Management
    email = request.form['email']
    password = request.form['password']
    try:
        user_data = db['User_Info'].find_one({"email": email})
        print(user_data)
        if user_data and user_data['password'] == password:
            # User found and password matches, set session data and redirect
            print(user_data)
            user_data = parse_json(user_data)
            session['sessionUser'] = user_data
            session['sessionUser']['userType']="admin"
            user_id = str(user_data['_id'])
            json_data = json.dumps({'_id': user_id})
            session['userId'] = json_data 
            print("hello")
            return redirect(url_for('adminDashboard'))  # Redirect to a generic dashboard
    except:
        session['signMess']="Please enter the correct credentials"
        return redirect(url_for('login')) 


# This will redirect the user to the customer signup page
@app.route('/customerSignup')
def customerSignup():
    message=session['signMess']
    session['signMess']="False"
    db = client.Area
    area_collection = db['areas'].find()
    area_dict = []
    for area_doc in area_collection:
        area_doc['_id'] = str(area_doc['_id'])  # Convert ObjectId to string
        area_dict.append(area_doc)

    return render_template('customerSignup.html', message=message,area_dict=area_dict)



@app.route('/signup/customer', methods=['POST'])
def customerSignUp():
    db = client.Customers
    print("Database connected")
    print(db.list_collection_names())
    collection = db.User_Info
    email = request.form['email']
    password = request.form['password']
    gender = request.form['gender']
    mobile = request.form['mobile']
    dob = request.form['dob']
    name = request.form['name']
    address = request.form['address']
    rating_data = [0,0.0,0.0]
    user_data = {
        "email": email,
        "password": password,
        "gender": gender,
        "mobile": mobile,
        "dob": dob,
        "name": name,
        "address": address,
        "rating": rating_data,
        "pendingOrderId": [],
        "signup_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Insert user data into MongoDB
    try:
        result = collection.insert_one(user_data)
        if result.inserted_id:
            session['signMess'] = 'Signup successful. Please login.'
            return redirect(url_for('login'))  # Redirect to login page after successful signup
        else:
            session['signMess'] = 'Failed to signup. Please try again.'
            return redirect(url_for('signUp'))  # Redirect to signup page if insertion fails
    except Exception as e:
        session['signMess'] = 'Error: ' + str(e)
        return redirect(url_for('signUp'))  # Redirect to signup page if exception occurs
    

# This will redirect to the signup page for the restaurant
@app.route('/restaurantSignup')
def restaurantSignup():
    message=session['signMess']
    session['signMess']="False"
    db = client.Area
    area_collection = db['areas'].find()
    area_dict = []
    for area_doc in area_collection:
        area_doc['_id'] = str(area_doc['_id'])  # Convert ObjectId to string
        area_dict.append(area_doc)
    return render_template('restaurantSignup.html', message=message,area_dict=area_dict)




@app.route('/signup/resturant', methods=['POST', 'GET'])
def restaurantsignup():
    db = client.Restaurant
    print(request.form['area'])
    email = request.form['email']
    password = request.form['password']
    area = request.form['area']
    name = request.form['name']
    session['signMess']="Fail"
    rating_data = [0,0.0,0.0]
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
    try:
        result = collection.insert_one(restaurant_data)
        if result.inserted_id:
            session['signMess'] = 'Signup successful. Please login.'
            return redirect(url_for('login'))  # Redirect to login page after successful signup
        else:
            session['signMess'] = 'Failed to signup. Please try again.'
            return redirect(url_for('signUp'))  # Redirect to signup page if insertion fails
    except Exception as e:
        session['signMess'] = 'Error: ' + str(e)
        return redirect(url_for('signUp'))  # Redirect to signup page if exception occurs
    



# This will redirect the user to the delivery agent signup page
@app.route('/deliveryAgentSignup')
def deliveryAgentSignup():
    message=session['signMess']
    session['signMess']="False"
    db = client.Area
    area_collection = db['areas'].find()
    area_dict = []
    for area_doc in area_collection:
        area_doc['_id'] = str(area_doc['_id'])  # Convert ObjectId to string
        area_dict.append(area_doc)
    return render_template('deliveryAgentSignup.html', message=message,area_dict=area_dict)

# This function will get the details for the delivery agent and store it in the database
@app.route('/signup/deliveryAgent', methods=['POST', 'GET'])
def deliveryAgentsignup():
    db = client.DeliveryAgent
    email = request.form['email']
    password = request.form['password']
    gender = request.form['gender']
    area = request.form['area']
    mobile = request.form['mobile']
    dob = request.form['dob']
    name = request.form['name']
    session['signMess']="Fail"
    rating_data = [0,0.0,0.0]
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
    # Insert user data into MongoDB
    collection = db['User_Info']
    try:
        result = collection.insert_one(deliveryAgent_data)
        if result.inserted_id:
            session['signMess'] = 'Signup successful. Please login.'
            return redirect(url_for('login'))  # Redirect to login page after successful signup
        else:
            session['signMess'] = 'Failed to signup. Please try again.'
            return redirect(url_for('signUp'))  # Redirect to signup page if insertion fails
    except Exception as e:
        session['signMess'] = 'Error: ' + str(e)
        return redirect(url_for('signUp'))  # Redirect to signup page if exception occurs

@app.route('/redirectDashboard')
def redirectDashboard():
    if session['sessionUser']['userType']=='customer':
        return redirect(url_for('customerDashboard'))
    elif session['sessionUser']['userType']=='restaurant':
        return redirect(url_for('restaurantDashboard'))
    elif session['sessionUser']['userType']=='deliveryAgent':
        return redirect(url_for('deliveryAgentDashboard'))
    elif session['sessionUser']['userType']=='admin':
        return redirect(url_for('adminDashboard'))

# These will be the routes for the Dashboard for the users
@app.route('/customerDashboard')
def customerDashboard():
    user=session['sessionUser']
    if user['userType'] == 'customer':
        print("yo")
        return render_template('customerDashboard.html', user=user)
    else:
        return redirect(url_for('logout'))
    

@app.route('/restaurantDashboard')
def restaurantDashboard():
    user=session['sessionUser']
    if user['userType'] == 'restaurant':
        print(user)
        return render_template('restaurantDashboard.html', user=user)
    else:
        return redirect(url_for('logout'))

@app.route('/deliveryAgentDashboard')
def deliveryAgentDashboard():
    user=session['sessionUser']
    if user['userType'] == 'deliveryAgent':
        return render_template('deliveryAgentDashboard.html', user=user)
    else:
        return redirect(url_for('logout'))

@app.route('/adminDashboard')
def adminDashboard():
    print("yo")
    user=session['sessionUser']
    if user['userType'] == 'admin':
        return render_template('adminDashboard.html', user=user)
    else:
        return redirect(url_for('logout'))


# This will show the personal data of the users
@app.route('/personalData')
# @check_token
def personalData():
    user=session['sessionUser']
    print(user)
    return render_template('personalData.html', user=user)


# This function will remove the data from the session and redirect to the login page
@app.route('/logout')
def logout():
    session.clear()
    session['signMess']="Successfully Logged Out"
    return redirect(url_for('login'))


# This will show the menu for the restaurant and a button to add food items
@app.route('/createMenu')
def createMenu():
    db = client.Restaurant
    user = session['sessionUser']
    if not user['userType'] == 'restaurant':
        return redirect(url_for('logout'))
    currResMenuId = session['userId']
    foodItemList = []
    food_items_collection = db['foodItem'].find({"restaurantId": currResMenuId})
    for item in food_items_collection:
        item['_id'] = str(item['_id'])  # Convert ObjectId to string for JSON serialization
        foodItemList.append(item)
    try:
        message = session['foodMessage']
        session['foodMessage'] = "False"
    except KeyError:
        session['foodMessage'] = "False"
        message = "False"
    return render_template('createMenu.html', user=user, menuList=foodItemList, message=message)


@app.route('/addFoodItem')
def addFoodItem():
    user = session['sessionUser']
    if user['userType'] == 'restaurant':
        message=session['foodMessage']
        session['foodMessage']="False"
        return render_template('addFoodItem.html', user=user, message=message)
    else:
        return redirect(url_for('logout'))


@app.route('/finishMenu')
def finishMenu():
    user = session['sessionUser']
    if user['userType']=='restaurant':
        return render_template('finishMenu.html', user=user)
    else:
        return redirect(url_for('logout'))


@app.route('/addFoodItem/adder', methods=['POST','GET'])
def foodItemAdder():
    if session['sessionUser']['userType'] != 'restaurant':
        return redirect(url_for('logout'))
    
    name = request.form['name']
    price = request.form['price']
    db = client.Restaurant
    try:
        restaurant_id = session["userId"]  # Get the restaurant ID
        print(type(restaurant_id))
        print(restaurant_id)
        foodItem = {
            "name": name,
            "pricePerItem": price,
            "isRecommended": False,
            "restaurantId": str(restaurant_id)
        }
        
        # Inserting the food item into the database for the specific restaurant
        inserted_food_item = db['foodItem'].insert_one(foodItem)
        
        # Get the inserted food item's ID
        food_item_id = str(inserted_food_item.inserted_id)
        session['foodMessage'] = "Food item text successfully added in database."
        return redirect(url_for('createMenu'))
    
    except Exception as e:
        print(e)
        session['foodMessage'] = "Error adding food item or uploading photo"
        return redirect(url_for('addFoodItem'))


@app.route('/allCustomers')
def allCustomers():
    user=session['sessionUser']
    if not user['userType']=="admin" and not user['userType']=='customer':
        return redirect(url_for('logout'))
    db = client.Customers
    customerList = []
    for customer in db['User_Info'].find():
        customer = parse_json(customer)
        temp_dict = customer
        customerList.append(temp_dict)
    session['customerList'] = customerList
    session.modified = True
    return render_template('allCustomers.html', user=user, customerList=customerList)

# This will create a list of the restaurant 
@app.route('/allRestaurant')
def allRestaurant():
    user = session['sessionUser']
    if not user['userType'] == 'admin' and not user['userType'] == 'customer':
        return redirect(url_for('logout'))
    db = client.Restaurant
    restaurantList = []
    for restaurant in db['Info'].find():
        restaurant = parse_json(restaurant)
        temp_dict = restaurant
        restaurantList.append(temp_dict)
    
    session['restaurantList'] = restaurantList
    session.modified = True
    return render_template('allRestaurant.html', user=user, restaurantList=restaurantList)

# This will create a list of all the delivery agents
@app.route('/allDeliveryAgents')
def allDeliveryAgents():
    user = session['sessionUser']
    if not user['userType'] == 'admin' and not user['userType'] == 'deliveryAgent':
        return redirect(url_for('logout'))
    db = client.DeliveryAgent
    deliveryAgentList = []
    for deliveryAgent in db['User_Info'].find():
        deliveryAgent = parse_json(deliveryAgent)
        temp_dict = deliveryAgent
        deliveryAgentList.append(temp_dict)
    session['deliveryAgentList'] = deliveryAgentList
    session.modified = True
    return render_template('allDeliveryAgents.html', user=user, deliveryAgentList=deliveryAgentList)

# This will show the food items in a restaurant, i.e. showing the menu of the restaurant
@app.route('/allFoodItem11/<restaurantUserId>')
def allFoodItem11(restaurantUserId):
    print("j")
    if not session['sessionUser']['userType'] == 'customer' and not session['sessionUser']['userType'] == 'admin':
        return redirect(url_for('logout'))
    session['currResMenuId']=restaurantUserId
    
    return redirect(url_for('allFoodItem'))



@app.route('/allFoodItem')
def allFoodItem():
    user = session['sessionUser']
    if not user['userType'] == 'customer' and not user['userType'] == 'admin':
        return redirect(url_for('logout'))
    
    foodItemList = []
    db = client.Restaurant
    restaurant_id = session['currResMenuId']
    restaurant_id = '{"_id": "' + restaurant_id + '"}'
    print(restaurant_id)
    food_items_collection = db['foodItem'].find({'restaurantId': restaurant_id})
    for food_item in food_items_collection:
        food_item = parse_json(food_item)
        foodItemList.append(food_item)
    session['currentMenu'] = foodItemList
    session.modified = True
    return render_template('allFoodItem.html', user=user, foodItemList=foodItemList)

# delete user from database
def deleteUserFromDatabase(to_delete,user_type):
    to_delete = str(to_delete)
    try:
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
    except :
        print("error deleting user from Database")
    
@app.route('/delete/<user_type>/<delete_id>')
def deleteUser(user_type, delete_id):
    if not session['sessionUser']['userType'] == "admin":
        return redirect(url_for('logout'))
    to_delete = int(delete_id)
    to_delete=to_delete-1
    if user_type == "restaurant":
        user_deleted=session['restaurantList'].pop(to_delete)
        session.modified = True
        deleteUserFromDatabase(user_deleted['_id'],"restaurant")
        return redirect(url_for('allRestaurant'))
    elif user_type == "customer":
        user_deleted = session['customerList'].pop(to_delete)
        session.modified = True
        deleteUserFromDatabase(user_deleted['_id'], "customer")
        return redirect(url_for('allCustomers'))
    elif user_type == 'deliveryAgent':
        user_deleted = session['deliveryAgentList'].pop(to_delete)
        session.modified = True
        deleteUserFromDatabase(user_deleted['_id'], "deliveryAgent")
        return redirect(url_for('allDeliveryAgents'))




@app.route('/order', methods=['POST','GET'])
def order():
    foodItemList = session['currentMenu']
    cost = 0
    orderList = []
    for i in range(len(foodItemList)):
        if not int(request.form[str(i+1)]) == 0:
            # print(foodItemList[i]['name'])
            foodItemList[i]['frequency'] = int(request.form[str(i+1)])
            foodItemList[i]['pricePerItem'] = int(foodItemList[i]['pricePerItem'])
            orderList.append(foodItemList[i])
            cost += int(foodItemList[i]['pricePerItem']) * int(foodItemList[i]['frequency'])  
    session['currentOrderCreating'] = {
            'orderList': orderList, 
            'isPending': True,
            'customerId': session['userId'],
            'restaurantId': session['currResMenuId'],
            'offerId': None,
            'orderValue': cost, 
            'discountValue':0,
            'deliveryCharge': 50,
            'orderDateTime': "",
            'deliveryAgentId' : "",
            'updateLevel' :0,
            'updateMessage' : "Accept/Reject",
            'orderUpdates' : [],
            'orderId': ''
    }
    return redirect(url_for('orderDetails'))

@app.route('/orderDetails')
def orderDetails():
    currentOrder = session['currentOrderCreating']
    db = client.Customers
    # Fetch customer name from MongoDB
    customer_id_str = currentOrder['customerId']
    extracted_string = customer_id_str[19:-4]
    customer_id = ObjectId(extracted_string)
    customer_doc = db['User_Info'].find_one({'_id': customer_id})
    customerName = customer_doc['name']
    db = client.Restaurant
    # Fetch restaurant name from MongoDB
    restaurant_id_str = currentOrder['restaurantId']
    restaurant_id_str = restaurant_id_str[10:-2]
    print(restaurant_id_str)
    restaurant_id = ObjectId(restaurant_id_str)
    restaurant_doc = db['Info'].find_one({'_id': restaurant_id})
    restaurantName = restaurant_doc['name']
    
    orderList = currentOrder['orderList']
    discount = currentOrder['discountValue']
    
    if currentOrder['offerId'] is None:
        offerUsed = None
        discount = 0
    else: 
        print("hi")
        customer_doc = client.Customers['User_Info'].find_one({'_id': customer_id})
        print(currentOrder['offerId'])
        offer_used_doc = None
        for offerID in customer_doc['promotionalOfferId']:
            print(offerID)
            if offerID == currentOrder['offerId']:
                offer_used_doc = client.Management['Offers'].find_one({'offerId': (offerID)})
                break
        offerUsed = offer_used_doc
        print('*',offerUsed)
        discount = min(int(int(currentOrder['orderValue']) * int(offerUsed['discount']) / 100), int(offerUsed['upperLimit']))

    final = max(currentOrder['orderValue'] + currentOrder['deliveryCharge'] - discount, 0)
    currentOrder['paidValue'] = final
    currentOrder['discountValue'] = discount

    return render_template('orderDetails.html', orderList=orderList, customerName=customerName, restaurantName=restaurantName, offerUsed=offerUsed, cost=currentOrder['orderValue'], deliveryCharge=currentOrder['deliveryCharge'], discount=discount, final=final)


@app.route('/placeOrder')
def placeOrder():
    currentOrder = session['currentOrderCreating']
    db = client.Orders
    order_collection = db['OrdersPlaced']
    order_result = order_collection.insert_one(currentOrder)
    orderId = order_result.inserted_id

    # Update the orderId field of the inserted document
    order_collection.update_one({'_id': orderId}, {'$set': {'orderId': str(orderId)}})

    # Add orderId to the restaurant's pendingOrderId array
    db = client.Restaurant
    restaurant_id_str = currentOrder['restaurantId']
    restaurant_id_str = restaurant_id_str[10:-2]
    restaurant_id = ObjectId(restaurant_id_str)
    restaurant_collection = db['Info']
    restaurant_collection.update_one({'_id': restaurant_id}, {'$push': {'pendingOrderId': orderId}})   
        

    # Add orderId to the customer's pendingOrderId array
    db = client.Customers
    customer_id_str = currentOrder['customerId']
    extracted_string = customer_id_str[19:-4]
    customer_id = ObjectId(extracted_string)
    customer_collection = db['User_Info']
    customer_collection.update_one({'_id': customer_id}, {'$push': {'pendingOrderId': orderId}})

    # If there's an offerId associated with the order, update order and remove offer from customer's collection
    if currentOrder['offerId'] is not None:
        offerId = currentOrder['offerId']
        customer_collection.update_one({'_id': customer_id}, {'$pull': {'promotionalOfferId': offerId}})
        order_collection.update_one({'_id': orderId}, {'$set': {'offerId': offerId}})

    # Redirect the user to the recentOrderCustomer route
    return redirect(url_for('recentOrderCustomer'))


@app.route('/recentOrderCustomer')
def recentOrderCustomer():
    user = session['sessionUser']
    customerId = session['userId']
    customerId = customerId[19:-4]
    customerId = ObjectId(customerId)
    print(customerId)
    # Fetch pending order IDs for the customer
    customer_db = client.Customers
    customer_collection = customer_db['User_Info']
    customer_data = customer_collection.find_one({'_id': customerId})
    
    if customer_data:
        listOrderId = customer_data.get('pendingOrderId', [])
        # Fetch recent orders for the customer
        order_db = client.Orders
        order_collection = order_db['OrdersPlaced']
        recentOrderList = []
        for order in order_collection.find({'_id': {'$in': listOrderId}}):
            temp = order
            # Fetch restaurant name for each order
            restaurant_id_str = temp['restaurantId'][10:-2]
            restaurant_id = ObjectId(restaurant_id_str)
            restaurant_data = client.Restaurant['Info'].find_one({'_id': restaurant_id})
            if restaurant_data:
                temp['restaurantName'] = restaurant_data.get('name')
            print(temp)
            temp = parse_json(temp)
            recentOrderList.append(temp)
        
        # Store recent orders in session
        session['presentOrderCustomer'] = recentOrderList
        session.modified = True
        print(recentOrderList)
        # Render template with recent order list
        return render_template('recentOrderCustomer.html', recentOrderList=recentOrderList)
    else:
        # Handle case where no pending orders found for the customer
        return "No pending orders found for the customer"


@app.route('/recentOrderRestaurant')
def recentOrderRestaurant():
    user = session['sessionUser']
    restaurantId = session['userId']
    restaurantId = restaurantId[19:-4]
    restaurantId = ObjectId(restaurantId)
    restaurant_data = client.Restaurant['Info'].find_one({'_id': restaurantId})
    if restaurant_data:
        listOrderId = restaurant_data.get('pendingOrderId', [])
        
        order_db = client.Orders
        order_collection = order_db['OrdersPlaced']
        recentOrderList = []
        for order in order_collection.find({'_id': {'$in': listOrderId}}):
            temp = order
            # Fetch customer name for each order
            customer_id_str = temp['customerId'][19:-4]
            customer_id = ObjectId(customer_id_str)
            customer_data = client.Customers['User_Info'].find_one({'_id': customer_id})
            if customer_data:
                temp['customerName'] = customer_data.get('name') # returns customer name
            temp = parse_json(temp)
            recentOrderList.append(temp)
        
        # Store recent orders in session
        session['presentOrderRestaurant'] = recentOrderList
        session.modified = True
        
        # Render template with recent order list
        return render_template('recentOrderRestaurant.html', recentOrderList=recentOrderList)
    else:
        # Handle case where no pending orders found for the restaurant
        return "No pending orders found for the restaurant"




@app.route('/orderDetailRestaurant/<orderId>')
def orderDetailRestaurant(orderId):
    orderId=int(orderId)
    if orderId > len(session['presentOrderRestaurant']):
        return redirect(url_for('recentOrderRestaurant'))
    orderId=orderId-1
    currentOrder=session['presentOrderRestaurant'][orderId]['orderId']
    currentOrder=client.Orders['OrdersPlaced'].find_one({'_id': ObjectId(currentOrder)})
    customer_id_str = currentOrder['customerId'][19:-4]
    customer_id = ObjectId(customer_id_str)
    customerName=client.Customers['User_Info'].find_one({'_id': (customer_id)})['name']
    restaurant_id_str = currentOrder['restaurantId'][10:-2]
    restaurant_id = ObjectId(restaurant_id_str)
    restaurantName=client.Restaurant['Info'].find_one({'_id': (restaurant_id)})['name']
    orderList=currentOrder['orderList']
    discount=currentOrder['discountValue']
    session['currentOrderUpdating']=currentOrder
    session.modified = True
    final=max(currentOrder['orderValue']+ currentOrder['deliveryCharge']- discount,0)
    currentOrder['_id']=str(currentOrder['_id'])
    return render_template('orderDetailsRestaurant.html', currentOrder = currentOrder, orderList=orderList, customerName=customerName, restaurantName=restaurantName, cost=currentOrder['orderValue'], deliveryCharge=currentOrder['deliveryCharge'], discount=discount, final=final, updateLevel=currentOrder['updateLevel'])

@app.route('/updateStatus0/<val>')
def updateStatus0(val):
    if session['sessionUser']['userType'] != 'restaurant':
        return redirect(url_for('logout'))

    if val == "Reject":
        update_order_dic = {'heading': "Rejected"}

        # Update order document
        order_collection = client.Orders['OrdersPlaced']
        order_id = session['currentOrderUpdating']['orderId']
        order_id = ObjectId(order_id)
        order_collection.update_one({'_id': order_id}, {'$push': {'orderUpdates': update_order_dic}})
        order_collection.update_one({'_id': order_id}, {'$set': {'isPending': False}})
        order_collection.update_one({'_id': order_id}, {'$set': {'updateMessage': "Rejected"}})
        order_collection.update_one({'_id': order_id}, {'$set': {'updateLevel': 1}})

        # Remove order from customer and restaurant pendingOrderId arrays
        customer_id = session['currentOrderUpdating']['customerId']
        customer_id = customer_id[19:-4]
        customer_id = ObjectId(customer_id)
        restaurant_id = session['currentOrderUpdating']['restaurantId']
        restaurant_id = restaurant_id[10:-2]
        restaurant_id = ObjectId(restaurant_id)
        client.Customers['User_Info'].update_one({'_id': customer_id}, {'$pull': {'pendingOrderId': order_id}})
        client.Restaurant['Info'].update_one({'_id': restaurant_id}, {'$pull': {'pendingOrderId': order_id}})

        return redirect(url_for('recentOrderRestaurant'))
    else:
        return render_template('getEstimatedTime.html')


@app.route('/getEstimatedTime', methods=['POST','GET'])
def getEstimatedTime():
    if session['sessionUser']['userType'] != 'restaurant':
        return redirect(url_for('logout'))
    try:
        estimatedTime = request.form['time']
        updateOrderDic = {
            'heading': "Accepted",
            'time' : str(estimatedTime)+" min"
        }
    except Exception as e:
        print(str(e))
    db = client.Orders
    try:
        order_id = session['currentOrderUpdating']['orderId']
        order_id = ObjectId(order_id)
        db['OrdersPlaced'].update_one(
            {'_id': order_id},
            {
                '$set': {'updateMessage': "Accepted. Preparing Food"},
                '$set': {'updateLevel': 1},
                '$push': {'orderUpdates': updateOrderDic}
            }
        )
    except Exception as e:
        print(str(e))
    return redirect(url_for('recentOrderRestaurant'))


@app.route('/updateStatus1')
def updateStatus1():
    if session['sessionUser']['userType'] != 'restaurant':
        return redirect(url_for('logout'))
    return render_template('foodPrepared.html')


@app.route('/updateStatus3')
def updateStatus3():
    if session['sessionUser']['userType'] != 'restaurant':
        return redirect(url_for('logout'))  
    currentOrder = session['currentOrderUpdating']
    db = client.Orders
    try:
        # Assuming 'order' is your collection name
        db['OrdersPlaced'].update_one(
            {'_id': ObjectId(currentOrder['orderId'])},
            {
                '$set': {'updateMessage': "Out for Delivery"},
                '$set': {'updateLevel': 4}
            }
        )
    except Exception as e:
        print(str(e))
    
    return redirect(url_for('recentOrderRestaurant'))


@app.route('/addPendingOrderId')
def addPendingOrderId():

    if session['sessionUser']['userType']!='restaurant':
        return redirect(url_for('logout'))

    pendingOrderId=session['currentOrderUpdating']['orderId']
    area=session['sessionUser']['area']
    try:
        db = client.Area
        db['areas'].update_one(
            {'name': area},
            {'$addToSet': {'availableOrderIdForPickup': pendingOrderId}}
        )
        db = client.Orders
        pendingOrderId = ObjectId(pendingOrderId)
        db['OrdersPlaced'].update_one(
            {'_id': pendingOrderId},
            {
                '$set': {'updateMessage': "Food is Prepared"},
                '$set': {'updateLevel': 2}
            }
        )
    except Exception as e:
        print(str(e))

    return redirect(url_for('recentOrderRestaurant'))


@app.route('/moreDetailsOrder<orderId>')
def moreDetailsOrder(orderId):
    if session['sessionUser']['userType'] != 'customer':
        return redirect(url_for('logout'))
    orderId=int(orderId)
    if orderId > len(session['presentOrderCustomer']):
        return redirect(url_for('recentOrderCustomer'))
    orderId=orderId-1
    currentOrder=session['presentOrderCustomer'][orderId]['orderId']
    # Query for the order
    db = client.Orders
    currentOrder = db['OrdersPlaced'].find_one({'_id': ObjectId(currentOrder)})
    currentOrder = parse_json(currentOrder)
    session['customerCurrentOrderChanging']=currentOrder
    if not currentOrder:
        return redirect(url_for('recentOrderCustomer'))
    
    # Additional queries to get customer and restaurant details
    db = client.Customers
    cus_str = currentOrder['customerId']
    cus_str = cus_str[19:-4]
    customer = db['User_Info'].find_one({'_id': ObjectId(cus_str)})
    db = client.Restaurant
    res_str = currentOrder['restaurantId']
    res_str = res_str[10:-2]
    restaurant = db['Info'].find_one({'_id': ObjectId(res_str)})
    
    orderList = currentOrder['orderList']
    offerUsed = None
    discount = 0
    
    if currentOrder['offerId']:
        db = client.Management
        offerUsed = db['Offers'].find_one({'_id': currentOrder['offerId']})
        if offerUsed:
            discount = min(int(currentOrder['orderValue']) * int(offerUsed['discount']) / 100, int(offerUsed['upperLimit']))
    
    final = max(currentOrder['orderValue'] + currentOrder['deliveryCharge'] - discount, 0)
    
    deliveryAgentName = ""
    if currentOrder['deliveryAgentId']:
        db = client.DeliveryAgent
        del_str = currentOrder['deliveryAgentId']
        del_str = del_str[19:-4]
        deliveryAgent = db['User_Info'].find_one({'_id': ObjectId(del_str)})
        if deliveryAgent:
            deliveryAgentName = deliveryAgent['name']
    
    return render_template('moreDetailsOrder.html', 
                           orderList=orderList, 
                           customerName=customer['name'], 
                           restaurantName=restaurant['name'], 
                           offerUsed=offerUsed, 
                           cost=currentOrder['orderValue'], 
                           deliveryCharge=currentOrder['deliveryCharge'], 
                           discount=discount, 
                           final=final, 
                           updateLevel=currentOrder['updateLevel'], 
                           orderUpdate=currentOrder['orderUpdates'], 
                           restaurantId=currentOrder['restaurantId'], 
                           customerId=currentOrder['customerId'], 
                           deliveryAgentName=deliveryAgentName)


@app.route('/useOffer<toUse>')
def useOffer(toUse):
    if session['sessionUser']['userType'] != 'customer':
        return redirect(url_for('logout'))
    user=session['userId']
    toUse=int(toUse)
    toUse=toUse-1
    session['currentOrderCreating']['offerId']=session['offerList'][toUse]['offerId']
    session.modified = True
    print(session['currentOrderCreating']['offerId'])
    return redirect(url_for('orderDetails'))


@app.route('/removeOfferFromOrder')
def removeOfferFromOrder():
    if session['sessionUser']['userType'] != 'customer':
        return redirect(url_for('logout'))
    session['currentOrderCreating']['offerId']=None
    session.modified = True
    return redirect(url_for('orderDetails'))

@app.route('/deleteFoodItem<foodItemId>')
def deleteFoodItem(foodItemId):
    if session['sessionUser']['userType'] != 'restaurant':
        return redirect(url_for('logout'))
    restaurantId=session['userId']
    try:
        db = client.Restaurant
        print(restaurantId)
        print(foodItemId)   
        foodItemId = ObjectId(foodItemId)
        food_item = db['foodItem'].find_one({'_id': foodItemId, 'restaurantId': restaurantId})
        print(food_item)
        result = db['foodItem'].delete_one(food_item)
        session['foodMessage'] = "Food item deletion from database is successful"
    except Exception as e:
        session['foodMessage'] = "Error deleting food item from database"

    return redirect(url_for('createMenu'))

@app.route('/recommendedRestaurant')
def recommendedRestaurant():
    user=session['sessionUser']
    if not user['userType'] == 'customer':
        return redirect(url_for('logout'))
    restaurantList = []
    tempRestaurantList = []
    # Assuming 'restaurant' is your collection name
    db = client.Restaurant
    docs = db['Info'].find()
    for doc in docs:
        doc = parse_json(doc)
        temp_dict = doc
        temp_dict['userId'] = str(doc['_id'])  
        temp_dict['areaName'] = doc['area']
        temp_dict['ratingValue'] = doc['rating'][2]
        tempRestaurantList.append(temp_dict)

    for restaurant in tempRestaurantList:
        if restaurant.get('isRecommended', False):
            restaurantList.append(restaurant)

    session['restaurantList'] = restaurantList
    session.modified = True

    return render_template('recommendedRestaurant.html', restaurantList=restaurantList, user=user)





@app.route('/createOffer')
def createOffer():
    user = session['sessionUser']
    if not user['userType'] == 'admin':
        return redirect(url_for('logout'))
    currentAdminId = session['userId']
    offerList = []
    db = client.Management
    # Fetch all offers from the MongoDB collection
    offer_collection = db['Offers']
    for offer in offer_collection.find():
        temp_dict = offer
        temp_dict['offerId'] = offer['_id'] 
        offerList.append(temp_dict)

    try:
        message=session['offerAdditionMessage']
        session['offerAdditionMessage']="False"
    except: 
        session['offerAdditionMessage']="False"
        message="False"
    return render_template('createOffer.html', user=user, offerList=offerList, message=message)

# This function will show the page to add offer and will show the input fields
@app.route('/addOffer')
def addOffer():
    if session['sessionUser']['userType'] != 'admin':
        return redirect(url_for('logout'))
    user = session['sessionUser']
    if user['userType'] == 'admin':
        message=session['offerAdditionMessage']
        session['offerAdditionMessage']="False"
        return render_template('addOffer.html', user=user, message=message)
    else:
        return redirect(url_for('logout'))

@app.route('/addOffer/adder', methods=['POST','GET'])
# @check_token
def offerAdder():
    if session['sessionUser']['userType'] != 'admin':
        return redirect(url_for('logout'))
    
    name = request.form['name']
    discount = request.form['discount']
    price = request.form['price']

    try:
        offer_id = ObjectId()
        offer_data = {
            "name": name,
            "discount": discount,
            "upperLimit": price,
            "offerId": str(offer_id)
        }
        db = client.Management
        # Assuming 'offer' is your collection name
        db['Offers'].insert_one(offer_data)

        session['offerAdditionMessage'] = "Offer added successfully."
        return redirect(url_for('createOffer'))

    except Exception as e:
        print(str(e))
        session['offerAdditionMessage'] = "Error adding offer to database"
        return redirect(url_for('addOffer'))


# This function will show all the offers to the customer in the frontend
@app.route('/allOffer<customer_id>')
def allOffer(customer_id):
    if session['sessionUser']['userType'] != 'admin':
        return redirect(url_for('logout'))
    
    customer_id = int(customer_id) - 1
    session['customerGettingOffer'] = session['customerList'][customer_id]['_id']

    offerList = []

    # Assuming 'offer' is your collection name
    db = client.Management
    docs = db['Offers'].find() # Fetch all offers
    for doc in docs:
        temp_dict = doc
        temp_dict['offerId'] = str(doc['_id'])  # Assuming offer id is stored as '_id'
        temp_dict = parse_json(temp_dict)
        offerList.append(temp_dict)

    session['offerList'] = offerList
    session.modified = True
    return render_template('allOfferAdmin.html', offerList=offerList)


# This function will give offer to the customer in the backend.
@app.route('/giveOffer<toGive>')
def giveOffer(toGive):
    if session['sessionUser']['userType'] != 'admin':
        return redirect(url_for('logout'))
    

    toGive=int(toGive)
    toGive=toGive-1

    customerGettingOffer=session['customerGettingOffer']
    offerId=session['offerList'][toGive]['offerId']
    customerGettingOffer = str(customerGettingOffer)
    try:
        # Fetch offer details from the 'offer' collection
        db = client.Management
        offer_data = db['Offers'].find_one({'_id': ObjectId(offerId)})
        db = client.Customers
        customerGettingOffer = customerGettingOffer[10:-2]
        db['User_Info'].update_one(
            {'_id': ObjectId(customerGettingOffer)},
            {'$push': {'promotionalOfferId': offer_data['offerId']}}
        )
    except Exception as e:
        print(str(e))
    return redirect(url_for('allCustomers'))


# This will show all the offers received by the customer from the admin
@app.route('/offerListCustomer')
def offerListCustomer():
    if session['sessionUser']['userType'] != 'customer':
        return redirect(url_for('logout'))
    user=session['userId']
    offerList=[]
    db = client.Customers
    user = user[19:-4]
    user = ObjectId(user)
    # Assuming 'customer' is your collection name
    customer_doc = db['User_Info'].find_one({'_id': user})
    if customer_doc:
        offer_ids = customer_doc.get('promotionalOfferId', [])
        for offer_id in offer_ids:
            offer_data = client.Management['Offers'].find_one({'offerId': (offer_id)})
            if offer_data:
                offer_data = parse_json(offer_data)
                offerList.append(offer_data)

    session['offerList'] = offerList
    session.modified = True

    return render_template('allOfferCustomer.html', offerList=offerList)


# This function will show all the past orders and details to the restaurant and the customers
@app.route('/pastOrder')
def pastOrder():
    if not session['sessionUser']['userType'] == 'restaurant' and not session['sessionUser']['userType'] == 'customer':
        return redirect(url_for('logout'))
    userId = session['userId']
    userType = session['sessionUser']['userType']
    pastOrderList = []
    docs = client.Orders['OrdersPlaced'].find()
    if userType == 'restaurant':
        res_str = userId
        userId = userId[9:-2]
    for order in docs:
        if not order['isPending']:
            print(order['restaurantId'])
            if userType == 'customer' and userId == order['customerId']:
                res_str = order['restaurantId']
                res_str = res_str[10:-2]
                restaurant = client.Restaurant['Info'].find_one({'_id': ObjectId(res_str)})
                if restaurant:
                    order['restaurantName'] = restaurant['name']
                    order = parse_json(order)
                    pastOrderList.append(order)
            elif userType == 'restaurant':
                if userId == order['restaurantId']:
                    cus_str = order['customerId']
                    cus_str = cus_str[19:-4]
                    customer = client.Customers['User_Info'].find_one({'_id': ObjectId(cus_str)})

                    if customer:
                        order['customerName'] = customer['name']
                        order = parse_json(order)
                        pastOrderList.append(order)
    print(pastOrderList)
    if userType == "customer":
        session['presentOrderCustomer'] = pastOrderList
        session.modified = True
        return render_template('pastOrderCustomer.html', pastOrderList=pastOrderList)
    elif userType == "restaurant":
        session['presentOrderRestaurant'] = pastOrderList
        session.modified = True
        return render_template('pastOrderRestaurant.html', pastOrderList=pastOrderList)


# This will show all the nearby delivery agent in the same area to the restaurant
@app.route('/nearbyDeliveryAgents')
def nearbyDeliveryAgents():
    if session['sessionUser']['userType']!='restaurant':
        return redirect(url_for('logout'))

    area=session['sessionUser']['area']
    nearbyDeliveryAgentsList=[]
    delivery_agents_in_area = client.DeliveryAgent['User_Info'].find({'area': area})
    for delivery_agent in delivery_agents_in_area:
        delivery_agent['areaName'] = area
        delivery_agent['ratingValue'] = delivery_agent['rating'][2]
        nearbyDeliveryAgentsList.append(delivery_agent)

    return render_template('nearbyDeliveryAgent.html', nearbyDeliveryAgentsList=nearbyDeliveryAgentsList)


# This function will show all the delivery requests for the delivery agent in the region sent by the restaurants
@app.route('/seeDeliveryRequest')
def seeDeliveryRequest():
    if session['sessionUser']['userType'] != 'deliveryAgent':
        return redirect(url_for('logout'))
    area = session['sessionUser']['area']
    db = client.Area
    print(area)
    area_data = db['areas'].find_one({'name': area})
    if 'availableOrderIdForPickup' in area_data:
        order_ids_for_pickup = area_data['availableOrderIdForPickup']
    else:
        order_ids_for_pickup = []

    deliveryRequestList = []
    for orderId in order_ids_for_pickup:
        db = client.Orders
        order_data = db['OrdersPlaced'].find_one({'_id': ObjectId(orderId)})
        if order_data and order_data.get('isPending', False):
            res_str = order_data['restaurantId']
            res_str = res_str[10:-2]
            order_data['restaurant'] = client.Restaurant['Info'].find_one({'_id': ObjectId(res_str)})
            cus_str = order_data['customerId']
            cus_str = cus_str[19:-4]
            order_data['customer'] = client.Customers['User_Info'].find_one({'_id': ObjectId(cus_str)})
            order_data['area'] = client.Area['areas'].find_one({'name': area})
            order_data = parse_json(order_data)
            deliveryRequestList.append(order_data)

    session['currentDeliveryRequest'] = deliveryRequestList
    session.modified = True

    return render_template("seeDeliveryRequest.html", deliveryRequestList=deliveryRequestList)


# This function will accept delivery request with getting the expected time of arrival and delivery from the delivery agent
# It will also update the status of the order to show to the customer
@app.route('/acceptDeliveryRequest', methods=['POST', 'GET'])
def acceptDeliveryRequest():
    if session['sessionUser']['userType']!='deliveryAgent':
        return redirect(url_for('logout'))
    
    time_to_reach_restaurant = request.form['timeToRestaurant']
    time_to_reach_customer = request.form['timeToCustomer']
    order_id = session['currentOrderDeliveryAgent']['orderId']
    print(order_id)
    client.Orders['OrdersPlaced'].update_one({'_id': ObjectId(order_id)}, {'$set': {
        'deliveryAgentId': session['userId'],
        'updateMessage': "Order Accepted by Delivery Agent",
        'updateLevel': 3,
        'orderUpdates': {
            '$push': {
                'timePickUp': time_to_reach_restaurant,
                'deliveryTime': time_to_reach_customer
            }
        }
    }})

    # Remove order ID from available orders for pickup in the delivery agent's area
    client.Area['areas'].update_one({'name': session['sessionUser']['area']}, {'$pull': {
        'availableOrderIdForPickup': order_id
    }})

    # Update delivery agent status and current order ID
    del_str = session['userId']
    del_str = del_str[19:-4]
    client.DeliveryAgent['User_Info'].update_one({'_id': ObjectId(del_str)}, {'$set': {
        'isAvailable': not session['sessionUser']['isAvailable'],
        'currentOrderId': order_id
    }})

    return redirect(url_for('moreDetailsDeliveryRequest', status="Details"))

# This function will show the details of the order and based on the statuses, the information on the front end will change
@app.route('/moreDetailsDeliveryRequest<status>')
def moreDetailsDeliveryRequest(status):

    if session['sessionUser']['userType']!='deliveryAgent':
        return redirect(url_for('logout'))
    
    # if the status is no order, no information is retrieved from the database, nor anything is displayed
    if status != "NoOrder":
        current_order_id = session['currentOrderDeliveryAgent']['orderId']
        db = client.Orders
        current_order = db['OrdersPlaced'].find_one({'_id': ObjectId(current_order_id)})
        session.modified = True
    showButton=3
    if status == "NoOrder":
        printTable = False
    else: 
        printTable = True
        # This showButton are to chose which button to show
        if status == "Accept":
            showButton = 1
        elif status == "Details" and session['currentOrderDeliveryAgent']['updateLevel'] == 4 :
            showButton = 2
        elif status == "Details" and session['currentOrderDeliveryAgent']['updateLevel']==2:
            showButton = 0
        else:
            showButton = 3
            
    currentOrder = None
    customerName = None
    restaurantName = None
    address = None
    orderList = None
    cost = None
    discount = None
    deliveryCharge = None
    final = None
    # Retrieving data from the database
    if status != "NoOrder":
        current_order_id = session['currentOrderDeliveryAgent']['orderId']
        current_order = client.Orders['OrdersPlaced'].find_one({'_id': ObjectId(current_order_id)})
        print(current_order)
        if current_order:
            cus_str = current_order['customerId']
            cus_str = cus_str[19:-4]
            customer = client.Customers['User_Info'].find_one({'_id': ObjectId(cus_str)})
            res_str = current_order['restaurantId']
            res_str = res_str[10:-2]
            restaurant = client.Restaurant['Info'].find_one({'_id': ObjectId(res_str)})
            if customer:
                customerName = customer['name']
                address = customer['address']
            if restaurant:
                restaurantName = restaurant['name']
            orderList = current_order['orderList']
            cost = current_order['orderValue']
            discount = int(current_order['discountValue'])
            deliveryCharge = current_order['deliveryCharge']
            final = current_order['orderValue']

    return render_template('moreDetailsDeliveryAgent.html', customerName=customerName, restaurantName=restaurantName, address = address, orderList=orderList, cost= cost, discount=discount, deliveryCharge=deliveryCharge, final= final, showButton = showButton, printTable = printTable)



# This function handles the change of location of the delivery agent
# We show the list of all the location to the delivery agent
@app.route('/markLocation')
def markLocation():
    if session['sessionUser']['userType']!='deliveryAgent':
        return redirect(url_for('logout'))
    db = client.Area
    area_dict = list(db['areas'].find())
    delivery_agent_id = session['userId']
    delivery_agent_id = delivery_agent_id[19:-4]
    delivery_agent_id = ObjectId(delivery_agent_id)
    current =client.DeliveryAgent['User_Info'].find_one({'_id': delivery_agent_id})
    current_area = current['area']
    return render_template("markLocation.html", area_dict=area_dict, currentArea=current_area)

@app.route('/updateArea', methods=['POST', 'GET'])
def updateArea():
    if session['sessionUser']['userType'] != 'deliveryAgent':
        return redirect(url_for('logout'))

    delivery_agent_id = session['userId']
    new_area = request.form['area']
    # Update the area of the delivery agent in the database
    db = client.DeliveryAgent
    print(delivery_agent_id)
    delivery_agent_id = delivery_agent_id[19:-4]
    delivery_agent_id = ObjectId(delivery_agent_id)
    print(delivery_agent_id)
    db['User_Info'].update_one({'_id': delivery_agent_id}, {'$set': {'area': new_area}})
    session['sessionUser']['area'] = new_area
    print(session['sessionUser']['area'])
    return redirect(url_for('deliveryAgentDashboard'))


# This function will show the order details for the order that the delivery agent chooses from the table
# will see the list from the one stored in session
@app.route('/orderDetailDeliveryAgent<orderId>')
def orderDetailDeliveryAgent(orderId):
    if session['sessionUser']['userType'] != 'deliveryAgent':
        return redirect(url_for('logout'))
    orderId=int(orderId)
    orderId = orderId-1
    session['currentOrderDeliveryAgent']=session['currentDeliveryRequest'][orderId]
    session.modified = True
    return redirect(url_for('moreDetailsDeliveryRequest', status = "Details"))



@app.route('/acceptOrderForDelivery')
def acceptOrderForDelivery():
    if session['sessionUser']['userType'] != 'deliveryAgent':
        return redirect(url_for('logout'))
    return redirect(url_for('moreDetailsDeliveryRequest', status = "Accept"))


@app.route('/currentOrderDeliveryAgent')
def currentOrderDeliveryAgent():
    if session['sessionUser']['userType'] != 'deliveryAgent':
        return redirect(url_for('logout'))
    user=session['sessionUser']
    db = client.DeliveryAgent
    del_str = session['userId']
    del_str = del_str[19:-4]
    current_order_id = db['User_Info'].find_one({'_id': ObjectId(del_str)})['currentOrderId']
    if not current_order_id:
        return redirect(url_for('moreDetailsDeliveryRequest', status="NoOrder"))
    else:
        db = client.Orders
        session['currentOrderDeliveryAgent'] = db['OrdersPlaced'].find_one({'_id': ObjectId(current_order_id)})
        session.modified = True
        session['currentOrderDeliveryAgent'] = parse_json(session['currentOrderDeliveryAgent'])
        return redirect(url_for('moreDetailsDeliveryRequest', status="Details"))



# This function rates the customer, and the rating is done by the deliveryagent
@app.route('/ratingDeliveryAgent', methods=['POST', 'GET'])
def ratingDeliveryAgent():
    
    # To prevent un-accessed use through links
    if session['sessionUser']['userType']!='deliveryAgent':
        return redirect(url_for('logout'))


    customerId=session['currentOrderDeliveryAgent']['customerId']
    customerId=customerId[19:-4]
    rating=request.form['customerRating']
    rating=int(rating)
    db = client.Customers
    customer = db['User_Info'].find_one({'_id': ObjectId(customerId)})
    ratingData = customer['rating']
    ratingData[0] = ratingData[0] + 1
    ratingData[1] = ratingData[1] + rating
    ratingData[2] = ratingData[1]/ratingData[0]
    
    currentOrder = session['currentOrderDeliveryAgent']

    # Update the order for the update done by the delivery agent and mention it as delivered
    order_id = currentOrder['orderId']

    # Update the order document
    client.Orders['OrdersPlaced'].update_one(
        {'_id': ObjectId(order_id)},
        {'$set': {
            'updateMessage': "Order Delivered",
            'updateLevel': 5,
            'isPending': False
        }}
    )

    # Update customer document to remove pending order ID
    customer_id = currentOrder['customerId']
    customer_id = customer_id[19:-4]
    client.Customers['User_Info'].update_one(
    {'_id': ObjectId(customer_id)},
    {
        '$pull': {'pendingOrderId': ObjectId(order_id)},
        '$set': {'rating': ratingData}
    }
)

    # Update restaurant document to remove pending order ID
    restaurant_id = currentOrder['restaurantId']
    restaurant_id = restaurant_id[10:-2]
    client.Restaurant['Info'].update_one(
        {'_id': ObjectId(restaurant_id)},
        {'$pull': {'pendingOrderId': ObjectId(order_id)}}
    )

    # Update delivery agent document
    delivery_agent_id = currentOrder['deliveryAgentId']
    delivery_agent_id = delivery_agent_id[19:-4]
    client.DeliveryAgent['User_Info'].update_one(
        {'_id': ObjectId(delivery_agent_id)},
        {'$set': {'isAvailable': True, 'currentOrderId': ""}}
    )

    # Reset the session
    session['currentOrderDeliveryAgent'] = None
    session.modified=True
    return redirect(url_for('deliveryAgentDashboard'))



@app.route('/ratingCustomer', methods=['POST', 'GET'])
def ratingCustomer():
    
    if session['sessionUser']['userType']!='customer':
        return redirect(url_for('logout'))


    orderId=session['customerCurrentOrderChanging']['orderId']
    db = client.Orders
    db['OrdersPlaced'].update_one(
        {'_id': ObjectId(orderId)},
        {'$set': {'updateLevel': 6}}
    )
    deliveryAgentId = db['OrdersPlaced'].find_one({'_id': ObjectId(orderId)})['deliveryAgentId']
    restaurantId = db['OrdersPlaced'].find_one({'_id': ObjectId(orderId)})['restaurantId']
    deliveryAgentId = deliveryAgentId[19:-4]
    deliveryAgentRating1=request.form['deliveryAgentRating']
    deliveryAgentRating1=int(deliveryAgentRating1)
    db = client.DeliveryAgent
    deliveryAgentRating=db['User_Info'].find_one({'_id': ObjectId(deliveryAgentId)})['rating']
    
    deliveryAgentRating[0] = deliveryAgentRating[0] + 1
    deliveryAgentRating[1] = deliveryAgentRating[1] + deliveryAgentRating1
    deliveryAgentRating[2] = deliveryAgentRating[1]/deliveryAgentRating[0]

    db['User_Info'].update_one(
        {'_id': ObjectId(deliveryAgentId)},
        {'$set': {'rating': deliveryAgentRating}}
    )    
    restaurantId = restaurantId[10:-2]
    restaurantRating1=request.form['restaurantRating']
    restaurantRating1=int(restaurantRating1)
    db = client.Restaurant
    restaurantRating=db['Info'].find_one({'_id': ObjectId(restaurantId)})['rating']
    

    restaurantRating[0] = restaurantRating[0] + 1
    restaurantRating[1] = restaurantRating[1] + restaurantRating1
    restaurantRating[2] = restaurantRating[1]/restaurantRating[0]

    db['Info'].update_one(
        {'_id': ObjectId(restaurantId)},
        {'$set': {'rating': restaurantRating}}
    )
    return redirect(url_for('pastOrder'))

# This will change the recommended status for the restaurant
@app.route('/changeRecommendRestaurant<id_to_change>')
def changeRecommendRestaurant(id_to_change):
    if session['sessionUser']['userType'] != 'admin':
        return redirect(url_for('logout'))
    id=int(id_to_change)
    id=id-1

    restaurantId=session['restaurantList'][id]['_id']
    restaurantId = str(restaurantId)
    if session['restaurantList'][id]['isRecommended'] == False:
        session['restaurantList'][id]['isRecommended'] = True
        session.modified = True
        
    else :
        session['restaurantList'][id]['isRecommended'] = False
        session.modified = True

    # change in database
    isRecommended=""
    try:
        db = client.Restaurant
        restaurants_collection = db['Info']
        restaurantId = restaurantId[10:-2]
        restaurantId = ObjectId(restaurantId)
        restaurant = restaurants_collection.find_one({"_id": restaurantId})
        isRecommended = restaurant.get('isRecommended', False)
    except Exception as e:
        print("error retriving isRecommended from database")
        pass
    
    try:
        restaurants_collection.update_one({"_id": restaurantId}, {"$set": {"isRecommended": not isRecommended}})
    except Exception as e:
        print("error changing isRecommended from database")
        pass

    return redirect(url_for('allRestaurant'))

# This function will change the recommend status of the food item, will be used by admin
@app.route('/changeRecommendFoodItem<id_to_change>')
def changeRecommendFoodItem(id_to_change):
    if session['sessionUser']['userType'] != 'admin':
        return redirect(url_for('logout'))
    id=int(id_to_change)
    id=id-1
    if session['currentMenu'][id]['isRecommended'] == False:
        session['currentMenu'][id]['isRecommended'] = True
        session.modified = True
    else :
        session['currentMenu'][id]['isRecommended'] = False
        session.modified = True
    foodItemId=session['currentMenu'][id]['_id']
    restaurantId = session['currentMenu'][id]['restaurantId']
    restaurantId = restaurantId[9:-2]
    print(restaurantId)
    foodItemId = str(foodItemId)
    isRecommended=""
    try:
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
        print("Error:", e)
    return redirect(url_for('allFoodItem11', restaurantUserId = restaurantId ))

if __name__ == "__main__":
    app.run(debug=True)
