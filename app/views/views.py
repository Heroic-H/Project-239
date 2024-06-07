from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from app.models.products import Products
from app.models.address import Address
from app.models.users import Users
from app.models.orders import Orders
from app.models.tickets import Tickets
from app import db

from flask_cors import cross_origin

views = Blueprint('views', __name__, url_prefix="/")

@views.route('/')
@cross_origin()
def login():
    try:
        return render_template("/login/login.html")
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

@views.route('/dashboard')
@cross_origin()
def dashboard():
    try:
        products = Products.query.all()
        return render_template("/dashboard/dashboard.html", products=products, user_id=session.get('user_id'))
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

@views.route('/profile')
@cross_origin()
def profile():
    try:
        user_id = session.get('user_id')
        user = Users.query.filter_by(id=user_id).first()
        order_query = f"select p.image, p.name, o.amount from products p right join orders o on o.user_id={user['id']} and p.id=o.product_id;"
#using the ['id'] and not .id leaves the page vulnerable to sql injection
        orders = db.engine.execute(order_query).all()
        tickets = Tickets.query.filter_by(user_id=user.id).all()
        addresses = Address.query.filter_by(user_id=user.id).all()
        return render_template("/profile/profile.html", user=user, orders=orders, addresses=addresses, tickets=tickets, user_id=user.id)
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

@views.route('/order')
@cross_origin()
def order():
    try:
        product_id = request.args.get("id")
        if not product_id:
            return jsonify({
                "message": "No product for purchase!",
                "status": "error"
            }), 400
        product = Products.query.filter_by(id=product_id).first()
        addresses = Address.query.filter_by(user_id=user.id).all()
        return render_template("/order/order.html", product=product, addresses=addresses, user_id=session.get('user_id'))
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

@views.route("/help")
@cross_origin()
def help_page():
    try:
        return render_template("/help/help.html", user_id=session.get('user_id'))
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

@views.route("/editor")
@cross_origin()
def editor():
    try:
        return render_template("/editor/editor.html")
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400
