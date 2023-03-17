"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken, Katie Byers.
"""

from flask import Flask, render_template, redirect, flash, session, request
import jinja2

import melons
import customers

app = Flask(__name__)

# A secret key is needed to use Flask sessioning features
app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.
app.jinja_env.undefined = jinja2.StrictUndefined

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """
    melon = melons.get_by_id(melon_id)

    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Melon successfully added to
    cart'."""
    
    session["cart"] = session.get("cart", {})
    session["cart"][melon_id] = session["cart"].get(melon_id, 0) + 1

    flash("Melon successfully added to cart.")

    return redirect("/cart")


@app.route("/cart")
def show_shopping_cart():
    """Display content of shopping cart."""

    if session.get('cart') == None:
        flash('There is nothing in your cart.')

        return render_template("cart.html", total_melons=[], order_cost=0)
    
    cart = session["cart"]
    total_melons = []
    order_cost = 0
  
    for melon_id, quantity in cart.items():
        melon = melons.get_by_id(melon_id)
        cost = melon.price * quantity
        order_cost += cost
        melon.quantity = quantity
        melon.cost = cost
        total_melons.append(melon)

    return render_template("cart.html", total_melons=total_melons, order_cost=order_cost)


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    # The logic here should be something like:
    #
    # - get user-provided name and password from request.form
    email = request.form.get("email")
    password = request.form.get("password")
    # - use customers.get_by_email() to retrieve corresponding Customer
    #   object (if any)
    customer = customers.get_by_email(email)
    # - if a Customer with that email was found, check the provided password
    #   against the stored one
    if customer is not None:
        if customer.password == password:
            session["logged_in_customer_email"] = customer.email
            flash("You are logged in.")
            return redirect("/melons")
        else:
            flash("Incorrect password.")
            return redirect("/login")
    else:
        flash("No customer with that email.")
        return redirect("/login")
    # - if they match, store the user's email in the session, flash a success
    #   message and redirect the user to the "/melons" route
    # - if they don't, flash a failure message and redirect back to "/login"
    # - do the same if a Customer with that email doesn't exist



@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3030)
