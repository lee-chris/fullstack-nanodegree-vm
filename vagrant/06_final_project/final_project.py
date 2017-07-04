from flask import Flask

app = Flask(__name__)

@app.route("/")
@app.route("/restaurants")
def view_restaurants():

    return "view all restaurants"


@app.route("/restaurants/new")
def create_restaurant():

    return "create new restaurant"


@app.route("/restaurants/delete/<int:restaurant_id>")
def delete_restaurant(restaurant_id):

    return "delete restaurant {0}".format(restaurant_id)


@app.route("/restaurants/edit/<int:restaurant_id>")
def edit_restaurant(restaurant_id):

    return "edit restaurant {0}".format(restaurant_id)


@app.route("/restaurants/<int:restaurant_id>")
def view_menu(restaurant_id):

    return "view menu for restaurant {0}".format(restaurant_id)


@app.route("/restaurants/<int:restaurant_id>/new")
def create_menu_item(restaurant_id):

    return "create new menu item for restaurant {0}".format(restaurant_id)


@app.route("/restaurants/<int:restaurant_id>/delete/<int:menu_item_id>")
def delete_menu_item(restaurant_id, menu_item_id):

    return "delete menu item {0} from restaurant {1}".format(menu_item_id, restaurant_id)


@app.route("/restaurants/<int:restaurant_id>/edit/<int:menu_item_id>")
def edit_menu_item(restaurant_id, menu_item_id):

    return "edit menu item {0} from restaurant {1}".format(menu_item_id, restaurant_id)


if __name__ == "__main__":
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host = "0.0.0.0", port = 5000)