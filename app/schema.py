from flask import Flask, request, jsonify
from pydantic import BaseModel, EmailStr, constr, ValidationError, Field
from typing import Literal, Optional
from datetime import date

class VisitorSignupSchema(BaseModel):
    phone: constr(pattern=r'^[0-9]{10,15}$')
    email: EmailStr
    password: constr(min_length=8, max_length=255)
    full_name: constr(min_length=2, max_length=100)
    dob: date
    gender: Literal["Male", "Female", "Other"]
    address: constr(min_length=5, max_length=500)
    city: constr(min_length=2, max_length=100)
    state: constr(min_length=2, max_length=100)
    country: constr(min_length=2, max_length=100)
    pincode: constr(pattern=r'^\d{6}$')
    nationality: constr(min_length=2, max_length=100)
    person_image: Optional[constr(max_length=255)] = None
    id_proof_type: Literal["Aadhar", "Passport", "VoterID", "DrivingLicense", "Other"]
    id_proof_number: constr(min_length=4, max_length=50)
    id_proof_photo: Optional[constr(max_length=255)] = None


class VisitorLoginSchema(BaseModel):
    email: EmailStr
    password: constr(max_length=255)
    
    
class VerifyOtpSchema(BaseModel):
    user_id: constr(min_length=1, max_length=3)
    phone: constr(min_length=4, max_length=50)
    email: constr(min_length=4, max_length=50)