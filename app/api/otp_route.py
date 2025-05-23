from flask import jsonify, request, Blueprint
from marshmallow import ValidationError
from app.services import OTPService
from app.schema import OTPGenerateSchema, OTPVerifySchema

otp = Blueprint('otp', __name__)

@otp.route("/generate_otp", methods=["POST"])
def generate_otp_route():
    json_data = request.get_json()
    delivery_method = json_data.get("delivery_method")

    schema = OTPGenerateSchema()
    try:
        data = schema.load(json_data)
        
        otp = OTPService.generate_otp()
        OTPService.store_otp(data["identifier"], otp, delivery_method)
        
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 409  # conflict for duplicate
    except Exception as err:
        return jsonify({"error": str(err)}), 500

    

    if delivery_method == "sms":
        print("sms send")
        #send_sms_otp(data["identifier"], otp)
    else:
        print("email send")
        #send_email_otp(data["identifier"], otp)

    return jsonify({"message": "OTP sent successfully."})


@otp.route("/verify_otp", methods=["POST"])
def verify_otp_route():
    json_data = request.get_json()
    delivery_method = json_data.get("delivery_method")

    schema = OTPVerifySchema()
    try:
        data = schema.load(json_data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except Exception as err:
        return jsonify({"error": str(err)}), 500

    if OTPService.verify_stored_otp(data["identifier"], data["otp"], delivery_method):
        return jsonify({"message": "OTP verified successfully."})
    else:
        return jsonify({"error": "Invalid or expired OTP."}), 400
