from flask import Blueprint, jsonify, request
from ..services.stripe_service import stripe
import os
from ..services.supabase_service import supabase

bp = Blueprint('payments', __name__, url_prefix='/payments')

#TODO must be changed everytime while testing
endpoint_secret= "whsec_e3d7b620f48b92afc2e8088c8104d249ed3f659475ee649ae3e07a862f1a3b51"

@bp.route('/create-stripe-session', methods=['POST'])
def create_session():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
    else:
        return jsonify({'status': 'Content-Type not supported!'})
    
    id = str(json)

    session = stripe.checkout.Session.create(
        mode="payment",
        success_url="http://localhost:5173/",
        cancel_url="http://localhost:5173/",
        line_items=[{
            "price": os.getenv("STRIPE_PRICE_ID"),
            "quantity": 1
        }],
        metadata= {
            "userId": id
        }
    )

    return jsonify({'sessionId': session.id})

@bp.route('/payment-successfull', methods=['POST'])
def payment_successful():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')

    event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
    )

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        user_id = session['metadata']['userId']

        try:
            supabase.table("user").update({"premium": "true"}).eq("user_id", user_id).execute()
        except Exception as e:
            print(f"Error during Supabase input (premium update): {e}")
            return jsonify({
                "status": False,
                "msg": 'There has been a problem upgrading your account - contact support'
            })

    return jsonify({'status': 'done'})