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


@app.route("/categories", methods = ["GET"])
def view_categories():
    """Display page of all product categories."""
    
    categories = item_dao.get_categories()
    return render_template("categories.html", categories = categories)


@app.route("/categories/new", methods = ["GET"])
def view_create_category_form():
    """Display form to create a new category."""
    
    return render_template("view_create_category_form.html")


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
    
    return render_template("view_update_category_form.html", category = category);


@app.route("/categories/<int:category_id>", methods = ["PUT"])
def update_category(category_id):
    """Handle request to update a product category."""
    
    category = Category()
    category.id = category_id
    category.name = request.form["name"]
    
    category = item_dao.edit_category(category)
    
    return jsonify(category.serialize)
    
    
if __name__ == "__main__":
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host = "0.0.0.0", port = 8000)
