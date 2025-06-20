from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from app.services import AuthService
from app.schema import RegistrationSchema, LoginSchema

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    schema = RegistrationSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify({"error": errors}), 400
    try:
        visitor = AuthService.register_visitor(data)
        return jsonify({
            "message": "Visitor registered successfully",
            "visitor": {
                "id": visitor.id,
                "email": visitor.email,
                "phone": visitor.phone,
                "full_name": visitor.full_name,
                "is_email_verified":visitor.is_email_verified
            }
        }), 201

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 409  # conflict for duplicate

    except Exception as e:
        return jsonify({"error": "Something went wrong"}), 500
    


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    schema = LoginSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400

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