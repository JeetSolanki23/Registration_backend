# ./app/api/auth/routes.py
from flask import jsonify, request
from flask_jwt_extended import create_access_token, set_access_cookies
from pydantic import ValidationError
from . import auth
from app.services import AuthService
from app.schema import VisitorSignupSchema, VisitorLoginSchema


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
                "full_name": visitor.full_name
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