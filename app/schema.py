from marshmallow import Schema, fields, validates, ValidationError, validate
import phonenumbers
from email_validator import validate_email, EmailNotValidError

# Validators
def validate_phone(value):
    try:
        number = phonenumbers.parse(value, None)
        if not phonenumbers.is_valid_number(number):
            raise ValidationError("Invalid phone number.")
    except phonenumbers.NumberParseException:
        raise ValidationError("Invalid phone number.")

def validate_email_address(value):
    try:
        validate_email(value)
    except EmailNotValidError:
        raise ValidationError("Invalid email address.")

# OTP Generate Schema
class OTPGenerateSchema(Schema):
    identifier = fields.String(required=True)
    type = fields.String(required=True, validate=validate.OneOf(["password_reset", "registration"]))
    delivery_method = fields.String(required=True, validate=validate.OneOf(["sms", "email"]))

    def validate(self, data, **kwargs):
        delivery_method = data.get("delivery_method")
        identifier = data.get("identifier")

        if not delivery_method or not identifier:
            raise ValidationError("Both 'identifier' and 'delivery_method' are required.")

        if delivery_method == "sms":
            validate_phone(identifier)
        elif delivery_method == "email":
            validate_email_address(identifier)
        else:
            raise ValidationError({"delivery_method": ["Invalid delivery method."]})


# OTP Verify Schema inherits generate and adds OTP field
class OTPVerifySchema(OTPGenerateSchema):
    otp = fields.String(required=True, validate=validate.Regexp(r"^\d{6}$", error="OTP must be exactly 6 digits"))

# Registration Schema
class RegistrationSchema(Schema):
    full_name = fields.String(required=True, validate=validate.Length(min=2))
    phone = fields.String(required=True, validate=validate_phone)
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    gender = fields.String(validate=validate.OneOf(["male", "female", "other"]))
    dob = fields.Date(required=True)
    address = fields.String(required=True, validate=validate.Length(min=5))
    city = fields.String(required=True)
    state = fields.String(required=True)
    country = fields.String(required=True)
    pincode = fields.String(required=True, validate=validate.Length(min=4, max=10))
    nationality = fields.String(required=True)
    #person_image = fields.String(required=True)  # base64, URL, or filepath
    id_proof_type = fields.String(required=True, validate=validate.OneOf(["passport", "driver_license", "aadhar", "voter_id", "other"]))
    id_proof_no = fields.String(required=True)
    #id_proof_image = fields.String(required=True)  # base64, URL, or filepath


class LoginSchema(Schema):
    email = fields.Email(required=True, error_messages={"required": "Email is required", "invalid": "Invalid email"})
    password = fields.String(
        required=True,
        error_messages={"required": "Password is required"}
    )


class PaymentVerificationSchema(Schema):
    razorpay_payment_id = fields.String(required=True, validate=validate.Length(min=1))
    razorpay_order_id = fields.String(required=True, validate=validate.Length(min=1))
    razorpay_signature = fields.String(required=True, validate=validate.Length(min=1))
