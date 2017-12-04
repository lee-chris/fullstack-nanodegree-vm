from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, make_response
from flask import session as login_session
from item_dao import ItemDao
from database_setup import Item, Category, User
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import json
import random
import requests
import string

app = Flask(__name__)
item_dao = ItemDao()

#Global variables used by gconnect
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template("login.html", STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    result = requests.get(url).json()
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    print("access_token={0}".format(access_token))

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        
        # replace existing access token with the most recent oauth token
        login_session['access_token'] = credentials.access_token
        
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    
    # Create user in db (if necessary)
    user_id = item_dao.getUserID(login_session['email'])
    if (user_id == None):
        print("creating new User entry")
        user_id = item_dao.createUser(login_session)
    
    login_session['user_id'] = user_id
    

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is {0}'.format(access_token))
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token={0}'.format(login_session['access_token'])
    print(url)
    result = requests.get(url)
    print('result is ')
    print(result)
    if result.status_code == 200:
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

	
@app.route("/")
@app.route("/catalog")
@app.route("/catalog/<int:category_id>")
def view_product_catalog(category_id = None):
    """Display main product catalog page."""
    
    categories = item_dao.get_categories(include_items = True)
    
    user_id = None
    if "user_id" in login_session:
        user_id = login_session["user_id"]
    
    if category_id is None:    
        return render_template("catalog.html", categories = categories, user_id = user_id)
    
    category = item_dao.get_category(category_id = category_id)
    items = item_dao.get_items(category_id = category_id)
    
    return render_template("catalog.html", categories = categories, category = category, items = items, user_id = user_id)


@app.route("/catalog/<int:category_id>/<int:item_id>")
def view_product(category_id, item_id):
    """Display the details page for a specific item."""
    
    category = item_dao.get_category(category_id = category_id)
    item = item_dao.get_item(item_id = item_id)
    
    return render_template("item.html", category = category, item = item)
    


@app.route("/catalog.json", methods = ["GET"])
def get_catalog():
    """Handle request to get full catalog."""
    
    categories = item_dao.get_categories(include_items = True)
    return jsonify(categories = [category.serialize_full for category in categories])


@app.route("/categories", methods = ["GET"])
def view_categories():
    """Display page of all product categories."""
    
    categories = item_dao.get_categories()
    return jsonify(categories = [category.serialize for category in categories])


@app.route("/categories/<int:category_id>", methods = ["GET"])
def get_category(category_id):
    """Handle request to get a specific category."""
    
    category = item_dao.get_category(category_id)
    
    if category is None:
        return jsonify({})
        
    return jsonify(category.serialize)


@app.route("/categories/admin", methods = ["GET"])
def view_categories_html():
    """Display page of all product categories."""
    
    categories = item_dao.get_categories()
    return render_template("categories.html", categories = categories)


@app.route("/categories/new", methods = ["GET"])
def view_create_category_form():
    """Display form to create a new category."""
    
    return render_template("category_create.html")


@app.route("/categories", methods = ["POST"])
def create_category():
    """Handle request to create a new product category."""
    
    category = Category()
    category.name = request.form["name"]
    
    category = item_dao.create_category(category)
    
    return jsonify(category.serialize)


@app.route("/categories/<int:category_id>/update", methods = ["GET"])
def view_update_category_form(category_id):
    """Display form to update a product category."""
    
    category = item_dao.get_category(category_id)
    
    return render_template("category_update.html", category = category);


@app.route("/categories/<int:category_id>", methods = ["PUT"])
def update_category(category_id):
    """Handle request to update a product category."""
    
    category = Category()
    category.id = category_id
    category.name = request.form["name"]
    
    category = item_dao.edit_category(category)
    
    return jsonify(category.serialize)


@app.route("/categories/<int:category_id>/delete", methods = ["GET"])
def view_delete_category_form(category_id):
    """Display form to delete a product category."""
    
    category = item_dao.get_category(category_id)
    
    return render_template("category_delete.html", category = category);


@app.route("/categories/<int:category_id>", methods = ["DELETE"])
def delete_category(category_id):
    """Handle request to delete a product category."""
    
    category = Category()
    category.id = category_id
    
    category = item_dao.delete_category(category)
    
    return jsonify(category.serialize)


@app.route("/items", methods = ["GET"])
def get_items():
    """Handle request to get items."""
    
    items = item_dao.get_items()
    
    return jsonify(items = [item.serialize for item in items])


@app.route("/items/<int:item_id>", methods = ["GET"])
def get_item(item_id):
    """Handle request get a specific item."""
    
    item = item_dao.get_item(item_id)
    
    if item is None:
        return jsonify({})
    
    return jsonify(item.serialize)


@app.route("/items/admin", methods = ["GET"])
def view_items_html():
    """Display page used to create, edit, delete items."""
    
    items = item_dao.get_items()
    
    return render_template("items.html", items = items)


@app.route("/items/new", methods = ["GET"])
def view_create_item_form():
    """Display html form used to create a new item."""
    
    categories = item_dao.get_categories()
    
    return render_template("item_create.html", categories = categories)


@app.route("/items", methods = ["POST"])
def create_item():
    """Handle request to create a new item."""
    
    item = Item()
    item.name = request.form["name"]
    item.category_id = request.form["category_id"]
    
    if request.form["description"] != "":
        item.description = request.form["description"]
    
    item = item_dao.create_item(item)
    
    return jsonify(item.serialize)


@app.route("/items/<int:item_id>/update", methods = ["GET"])
def view_update_item_form(item_id):
    """Display html form to update an item."""
    
    categories = item_dao.get_categories()
    item = item_dao.get_item(item_id)
    
    return render_template("item_update.html", item = item, categories = categories)


@app.route("/items/<int:item_id>", methods = ["PUT"])
def update_item(item_id):
    """Handle request to update an item."""
    
    item = Item()
    
    item.id = item_id
    item.name = request.form["name"]
    item.category_id = request.form["category_id"]
    
    if request.form["description"] != "":
        item.description = request.form["description"]
    
    item = item_dao.edit_item(item)
    
    return jsonify(item.serialize)


@app.route("/items/<int:item_id>/delete", methods = ["GET"])
def view_delete_item_form(item_id):
    """Display html form to delete an item."""
    
    item = item_dao.get_item(item_id)
    
    return render_template("item_delete.html", item = item)


@app.route("/items/<int:item_id>", methods = ["DELETE"])
def delete_item(item_id):
    """Handle request to delete an item."""
    
    item = Item()
    item.id = item_id
    
    item = item_dao.delete_item(item)
    
    return jsonify(item.serialize)
    
    
if __name__ == "__main__":
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host = "0.0.0.0", port = 8000)
