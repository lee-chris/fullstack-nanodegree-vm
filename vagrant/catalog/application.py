from flask import Flask, render_template
from item_dao import ItemDao

app = Flask(__name__)
item_dao = ItemDao()

@app.route("/")
def view_product_catalog():
    
    items = item_dao.get_items()
    return render_template("catalog.html", items = items)


if __name__ == "__main__":
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host = "0.0.0.0", port = 8000)
