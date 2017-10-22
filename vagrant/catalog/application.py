from flask import Flask, render_template, request, redirect, url_for, jsonify
from item_dao import ItemDao
from database_setup import Item, Category

app = Flask(__name__)
item_dao = ItemDao()

@app.route("/")
def view_product_catalog():
    """Display main product catalog page."""
    
    items = item_dao.get_items()
    return render_template("catalog.html", items = items)


@app.route("/catalog", methods = ["GET"])
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
