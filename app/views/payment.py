import stripe
import json
from app.models.user import User
from flask import jsonify, url_for, redirect, render_template, request
from flask_login import current_user
from app.views import bp
import os

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
endpoint_secret = os.environ.get("STRIPE_ENDPOINT_SECRET")


@bp.route('/webhook', methods=['POST'])
def webhook():
    event = None
    payload = request.data
    try:
        event = json.loads(payload)
    except Exception as e:
        print('Webhook error while parsing basic request.' + str(e))
        return jsonify(success=True)
    if endpoint_secret:
        # Only verify the event if there is an endpoint secret defined
        # Otherwise use the basic event deserialized with json
        sig_header = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except stripe.error.SignatureVerificationError as e:
            print('⚠️  Webhook signature verification failed.' + str(e))
            return jsonify(success=True)

    # Handle the event
    if event and event['type'] == 'checkout.session.completed':
        print("checkout session completed")
        checkout_session_object = event['data']['object']  # contains a stripe.CheckoutSession
        # print(json.dumps(checkout_session_object, indent=2))
        user_id = checkout_session_object["metadata"]["user_id"]
        user_email = checkout_session_object["metadata"]["user_email"]
        payment_intent = checkout_session_object["payment_intent"]
        # Then define and call a method to handle the successful payment intent.
        # handle_payment_intent_succeeded(payment_intent)
        user = User.get_or_none(id=user_id, email=user_email)
        if user:
            user.payment_intent = payment_intent
            user.update_expiration_date()
            user.save()
    else:
        # Unexpected event type
        print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)


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
