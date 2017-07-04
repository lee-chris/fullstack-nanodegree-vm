from flask import Flask, render_template

app = Flask(__name__)

# static db objects
restaurants = [{"id" : 0, "name" : "Burger King"}, {"id" : 1, "name" : "Pizza Hut"}]
menu_items = [[{"id" : 0, "name" : "Whopper", "price" : "$2.99"}], [{"id" : 0, "name" : "Meat Lovers", "price" : "$10.99"}, {"id" : 1, "name" : "Veggie Lovers", "price" : "$9.99"}]]

@app.route("/")
@app.route("/restaurants")
def view_restaurants():

    return render_template("restaurants.html", restaurants = restaurants)


@app.route("/restaurants/new")
def create_restaurant():

    return render_template("new_restaurant.html")


@app.route("/restaurants/delete/<int:restaurant_id>")
def delete_restaurant(restaurant_id):

    return render_template("delete_restaurant.html", restaurant = restaurants[restaurant_id])


@app.route("/restaurants/edit/<int:restaurant_id>")
def edit_restaurant(restaurant_id):

    return render_template("edit_restaurant.html", restaurant = restaurants[restaurant_id])


@app.route("/restaurants/<int:restaurant_id>/menu")
def view_menu(restaurant_id):

    return render_template("view_menu.html", restaurant = restaurants[restaurant_id], items = menu_items[restaurant_id])


@app.route("/restaurants/<int:restaurant_id>/menu/new")
def create_menu_item(restaurant_id):

    return "create new menu item for restaurant {0}".format(restaurant_id)


@app.route("/restaurants/<int:restaurant_id>/menu/delete/<int:menu_item_id>")
def delete_menu_item(restaurant_id, menu_item_id):

    return "delete menu item {0} from restaurant {1}".format(menu_item_id, restaurant_id)


@app.route("/restaurants/<int:restaurant_id>/menu/edit/<int:menu_item_id>")
def edit_menu_item(restaurant_id, menu_item_id):

    return "edit menu item {0} from restaurant {1}".format(menu_item_id, restaurant_id)


if __name__ == "__main__":
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host = "0.0.0.0", port = 5000)
