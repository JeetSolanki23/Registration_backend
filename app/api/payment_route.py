from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schema import PaymentVerificationSchema
from app.services.payment_service import create_payment_order, verify_payment_signature

payment = Blueprint('payment', __name__)

@payment.route('/create-order', methods=['POST'])
@jwt_required()
def create_order():
    try:
        order = create_payment_order()
        return jsonify({
            "order_id": order['id'],
            "amount": order['amount'],
            "currency": order['currency'],
            "key": current_app.config['RAZORPAY_KEY_ID']
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500