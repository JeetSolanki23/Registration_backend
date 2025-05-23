from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schema import PaymentVerificationSchema
from app.services.payment_service import create_payment_order, verify_razorpay_payment

payment = Blueprint('payment', __name__)

@payment.route('/create_order', methods=['POST'])
@jwt_required()
def create_order():
    try:
        visitor_id = get_jwt_identity()
        order = create_payment_order(visitor_id)
        return jsonify({
            "order_id": order['id'],
            "amount": order['amount']/100,
            "currency": order['currency'],
            "key": current_app.config['RAZORPAY_KEY_ID']
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
        
@payment.route("/verify_payment", methods=["POST"])
@jwt_required()
def verify_payment():
    try:
        json_data = request.get_json()
        schema = PaymentVerificationSchema()
        errors = schema.validate(json_data)
        if errors:
            return jsonify(errors), 400

        visitor_id = get_jwt_identity()
        result = verify_razorpay_payment(
        visitor_id=visitor_id,
        razorpay_payment_id=json_data["razorpay_payment_id"],
        razorpay_order_id=json_data["razorpay_order_id"],
        razorpay_signature=json_data["razorpay_signature"]
    )

        status_code = 200 if result["verified"] else 400
        return jsonify({"status": result["message"]}), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500
