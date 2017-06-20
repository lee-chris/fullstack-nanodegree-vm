from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)


engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route("/")
@app.route("/restaurants/<int:restaurant_id>/")
def HelloWorld(restaurant_id):

    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)

    return render_template("menu.html", restaurant = restaurant, items = items)

@app.route("/restaurants/<int:restaurant_id>/new")
def newMenuItem(restaurant_id):
    return "page to create a new menu item."

@app.route("/restaurants/<int:restaurant_id>/<int:menu_item>/edit")
def editMenuItem(restaurant_id, menu_item):
    return "page to edit a menu item."

@app.route("/restaurants/<int:restaurant_id>/<int:menu_id>/delete")
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item."

if __name__ == "__main__":
    app.debug = True
    app.run(host = "0.0.0.0", port = 5000)
