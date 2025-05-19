# ./app/api/auth/routes.py
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from pydantic import ValidationError
from . import auth
from app.services import AuthService
from app.schema import VisitorSignupSchema, VisitorLoginSchema, VerifyOtpSchema


@auth.route('/register', methods=['POST'])
def signup():
    try:
        data = VisitorSignupSchema(**request.get_json())
        visitor = AuthService.register_visitor(data)
        return jsonify({
            "message": "Visitor registered successfully",
            "visitor": {
                "id": visitor.id,
                "email": visitor.email,
                "phone": visitor.phone,
                "full_name": visitor.full_name,
                "is_phone_verified":visitor.is_phone_verified,
                "is_email_verified":visitor.is_email_verified
            }
        }), 201

    except ValidationError as e:
        error_dict = {}
        for err in e.errors():
            field = ".".join(str(loc) for loc in err['loc'])
            error_dict[field] = err['msg']
        return jsonify({"errors": error_dict}), 400

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 409  # conflict for duplicate

    except Exception as e:
        return jsonify({"error": "Something went wrong"}), 500

        
        
@auth.route('/login', methods=['GET', 'POST'])
def login():
    try:
        data = VisitorLoginSchema(**request.get_json())
    except ValidationError as e:
        errors = {err['loc'][0]: err['msg'] for err in e.errors()}
        return jsonify({"errors": errors}), 400

    result, error = AuthService.login_visitor(data)
    if error:
        return jsonify({"error": error}), 401

    return jsonify(result), 200
    

@auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


@auth.route('/verifyOtp', methods=['POST'])
def verify_otp():
    data = VerifyOtpSchema(**request.get_json())
    email, phone = AuthService.verify_otp(data)
    return jsonify({"user_id": data.user_id,
        "is_email_verified":email,
        "is_phone_verified":phone
    })

@auth.route('/profile', methods=['POST'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    return jsonify({"message": f"Welcome user {user_id}"})
