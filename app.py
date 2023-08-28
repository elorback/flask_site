# Team Member: Manpreet Dhindsa
# Team Member: Eric Lorback
# Team Member: Brian Kelly

# Importing Flask and other modules
from flask import Flask, request, render_template, jsonify, redirect, session
import sql # This is our sql.py file
 
# Flask constructor
app = Flask(__name__)  
app.secret_key = "my_secret_key"

# Global Variables
logged_in_username = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/logout", methods=["GET"])
def logout():
    session.clear()  # Clear the session data to log the user out
    return redirect("/")

@app.route("/initalizeDatabase", methods=["GET"])
def initalizeDatabase():
    sql.initalizeDatabase()
    return jsonify({"result": True}) 

@app.route("/home", methods=["GET"])
def home():
    if not session.get("logged_in"):
        return redirect("/")
    return render_template("home.html")

@app.route('/api/login', methods=['POST'])
def api_login():
    print("In the Python login method")
    data = request.get_json()
    print(data)
    global logged_in_username

    username = data["param1"]
    password = data["param2"]

    sql.create_database_if_not_exists()
    sql.create_user_table_if_not_exists()
    result = sql.check_user_credentials(username, password)    
    print("In APP.py")
    print(result)
    if result:
        session["logged_in"] = True
        logged_in_username = result
        return jsonify({"result": True})  # Return a JSON response indicating success
    else:
        return jsonify({"result": False, "message": "Invalid credentials"})

@app.route('/api/insertItem', methods=['POST'])
def api_insertItem():
    print("In the Python insertItem method")
    data = request.get_json()
    print(data)

    title = data["param1"]
    description = data["param2"]
    categories = data["param3"]
    price = data["param4"]

    sql.create_schema_if_not_exists()
    result = sql.insertItem(title, description, categories, price)   
    print("In APP.py")
    print(result)
    if result:
        return jsonify({"result": True})  # Return a JSON response indicating success
    else:
        return jsonify({"result": False, "message": "User already reached 3 items posted today!"})

@app.route('/api/signup', methods=['POST'])
def api_signup():
    print("In the Python signup method")
    data = request.get_json()
    print(data)

    username = data["param1"]
    password = data["param2"]
    fname = data["param3"]
    lname = data["param4"]
    email = data["param5"]

    sql.create_database_if_not_exists()
    sql.create_user_table_if_not_exists()
    result = sql.add_new_user(username, password, fname, lname, email)

    return jsonify({"result": result})

@app.route('/get_users')
def get_users():
    users = sql.get_all_users()
    if users is not None:
        return jsonify(users)
    else:
        return jsonify([])

@app.route('/get_global_var')
def get_global_var():
    return jsonify({'value': logged_in_username})

@app.route("/get_category_items", methods=['POST'])
def get_category_items():
    data = request.get_json()
    print(data)

    category = data["param1"]

    users = sql.get_category_items(category)

    if users is not None:
        return jsonify(users)
    else:
        return jsonify([])

@app.route('/api/insertReview', methods=['POST'])
def insertReview():
    print("In the Python insertReview method")
    data = request.get_json()
    print(data)

    reviewer_username = data["param1"]
    itemID = data["param2"]
    selectedRankValue = data["param3"] # Excellent, Good, Fair, Bad
    reviewDescription = data["param4"]

    sql.create_schema_if_not_exists()
    result = sql.insertReview(reviewer_username, itemID, selectedRankValue, reviewDescription)   
    print("In APP.py insert Review method")
    print(result)
    if result:
        return jsonify({"result": True})  # Return a JSON response indicating success
    else:
        return jsonify({"result": False, "message": "User already reached 3 items posted today!"})

@app.route("/get_phase3_1", methods=['GET'])
def get_phase3_1():
    items = sql.get_phase3_1()

    if items is not None:
        return jsonify(items)
    else:
        return jsonify([])

@app.route("/get_phase3_2", methods=['POST'])
def get_phase3_2():
    data = request.get_json()
    print(data)

    c1 = data["param1"]
    c2 = data["param2"]

    items = sql.get_phase3_2(c1, c2)

    if items is not None:
        return jsonify(items)
    else:
        return jsonify([])

@app.route("/get_phase3_3", methods=['POST'])
def get_phase3_3():
    data = request.get_json()
    print(data)

    username = data["param1"]

    items = sql.get_phase3_3(username)

    if items is not None:
        return jsonify(items)
    else:
        return jsonify([])

@app.route("/get_phase3_4", methods=['GET'])
def get_phase3_4():
    items = sql.get_phase3_4()

    if items is not None:
        return jsonify(items)
    else:
        return jsonify([])

@app.route("/get_phase3_5", methods=['GET'])
def get_phase3_5():
    items = sql.get_phase3_5()

    if items is not None:
        return jsonify(items)
    else:
        return jsonify([])

@app.route("/get_phase3_6", methods=['GET'])
def get_phase3_6():
    items = sql.get_phase3_6()

    if items is not None:
        return jsonify(items)
    else:
        return jsonify([])

if __name__ == '__main__':
   app.run(debug=True)
