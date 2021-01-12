import stripe
from flask import jsonify, url_for, redirect, render_template
from flask_login import current_user
from app.views import bp
import os

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")


@bp.route('/payment-success', methods=['GET', 'POST'])
def payment_success():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return render_template('views/payment_success.html')


@bp.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    if not current_user.is_authenticated:
        return "No one is logged in to create a checkout session", 401
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': 300,
                        'product_data': {
                            'name': 'Personal Scoreboard - 1 Year Access',
                            'images': ["https://i.ibb.co/HPxfYmJ/Screen-Shot-2021-01-06-at-11-23-41-PM.png"]
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            customer_email=current_user.email,
            metadata={'user_id': current_user.id, "user_email": current_user.email},
            success_url=url_for("views.payment_success", _external=True),
            cancel_url=url_for("views.account", _external=True)
        )
        return jsonify({'id': checkout_session.id})
    except Exception as e:
        print(e)
        return jsonify(error=str(e)), 403
