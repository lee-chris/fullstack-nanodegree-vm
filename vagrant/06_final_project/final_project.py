from flask import Flask, render_template, request, redirect, url_for

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)
engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

# static db objects
restaurants = [{"id" : 0, "name" : "Burger King"}, {"id" : 1, "name" : "Pizza Hut"}]
menu_items = [[{"id" : 0, "name" : "Whopper", "price" : "$2.99"}], [{"id" : 0, "name" : "Meat Lovers", "price" : "$10.99"}, {"id" : 1, "name" : "Veggie Lovers", "price" : "$9.99"}]]

@app.route("/")
@app.route("/restaurants")
def view_restaurants():

    # query for all restaurants
    session = DBSession()
    restaurants = session.query(Restaurant).all()
    
    return render_template("restaurants.html", restaurants = restaurants)


@app.route("/restaurants/new", methods=["GET", "POST"])
def create_restaurant():

    if request.method == "GET":
        return render_template("new_restaurant.html")

    elif request.method == "POST":

        session = DBSession()
        restaurant = Restaurant(name = request.form["name"])
        session.add(restaurant)
        session.commit()

        return redirect(url_for("view_restaurants"))


@app.route("/restaurants/delete/<int:restaurant_id>", methods=["GET", "POST"])
def delete_restaurant(restaurant_id):

    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    
    if request.method == "GET":
        return render_template("delete_restaurant.html", restaurant = restaurant)

    elif request.method == "POST":

        session.delete(restaurant)
        session.commit()

        return redirect(url_for("view_restaurants"))


@app.route("/restaurants/edit/<int:restaurant_id>", methods=["GET", "POST"])
def edit_restaurant(restaurant_id):

    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()

    if request.method == "GET":
        return render_template("edit_restaurant.html", restaurant = restaurant)

    elif request.method == "POST":

        restaurant.name = request.form["name"]

        session.add(restaurant)
        session.commit()

        return redirect(url_for("view_restaurants"))


@app.route("/restaurants/<int:restaurant_id>/menu")
def view_menu(restaurant_id):

    return render_template("view_menu.html", restaurant = restaurants[restaurant_id], items = menu_items[restaurant_id])


@app.route("/restaurants/<int:restaurant_id>/menu/new")
def create_menu_item(restaurant_id):

    return render_template("new_menu_item.html", restaurant = restaurants[restaurant_id])


@app.route("/restaurants/<int:restaurant_id>/menu/delete/<int:menu_item_id>")
def delete_menu_item(restaurant_id, menu_item_id):

    return render_template("delete_menu_item.html", restaurant = restaurants[restaurant_id], item = menu_items[restaurant_id][menu_item_id])


@app.route("/restaurants/<int:restaurant_id>/menu/edit/<int:menu_item_id>")
def edit_menu_item(restaurant_id, menu_item_id):

    return render_template("edit_menu_item.html", restaurant = restaurants[restaurant_id], item = menu_items[restaurant_id][menu_item_id])


if __name__ == "__main__":
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host = "0.0.0.0", port = 5000)
