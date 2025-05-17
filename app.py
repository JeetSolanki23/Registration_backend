from flask import Flask, request, jsonify
from pydantic import ValidationError, BaseModel, EmailStr, StringConstraints
from typing import Annotated

PhoneStr = Annotated[str, StringConstraints(pattern=r'^\+?\d{10,15}$')]
PasswordStr = Annotated[str, StringConstraints(min_length=6)]

class RegisterSchema(BaseModel):
    name: str
    email: EmailStr
    phone: PhoneStr
    password: PasswordStr
    confirm_password: str




app = Flask(__name__)

@app.route('/api/register', methods=['POST'])
def register():
    try:
        user = RegisterSchema(**request.get_json())

        if user.password != user.confirm_password:
            return jsonify({"error": "Passwords do not match"}), 400

        return jsonify({
            "message": "User registered successfully",
            "user": {
                "name": user.name,
                "email": user.email,
                "phone": user.phone
            }
        }), 201

    except ValidationError as e:
        # Strip out 'url' field from each error
        errors = []
        for err in e.errors():
            err.pop('url', None)
            errors.append(err)
        return jsonify({"errors": errors}), 400

if __name__ == '__main__':
    app.run(debug=True)
