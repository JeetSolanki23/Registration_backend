# ./app/services/auth_services.py
from app.extensions import db
from app.models import *


class AuthService:
    
    @staticmethod
    def save_file(file):
        if not file:
            return None
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        return path
    
    
    @staticmethod
    def ragistor(form):
        """ragistor user."""
        if form.validate_on_submit():
            with db.session.begin():
                stmt = select(Visitor).where(
                    (Visitor.email == form.email.data) | 
                    (Visitor.phone == form.phone.data)
                )
                existing = db.session.execute(stmt).scalars().first()
                if existing:
                    return jsonify({"error": "Email or phone already registered."}), 409
    
                visitor = Visitor(
                    phone=form.phone.data,
                    email=form.email.data,
                    password=visitor.set_password(form.password.data),
                    full_name=form.full_name.data,
                    dob=form.dob.data,
                    age=form.age.data,
                    gender=form.gender.data,
                    address=form.address.data,
                    city=form.city.data,
                    state=form.state.data,
                    country=form.country.data,
                    pincode=form.pincode.data,
                    nationality=form.nationality.data,
                    person_image=save_file(request.files.get('person_image')),
                    id_proof_type=form.id_proof_type.data,
                    id_proof_number=form.id_proof_number.data,
                    id_proof_photo=save_file(request.files.get('id_proof_photo'))
                )
                db.session.add(visitor)
    
            return jsonify({"message": "Visitor registered successfully!", "id": visitor.id}), 201
        else:
            return jsonify({"errors": form.errors}), 400

    @staticmethod
    def login(form):
        """Authenticate and log in a user."""
        if form.validate_on_submit():
            stmt = select(Visitor).where(Visitor.email == form.email.data)
            visitor = db.session.execute(stmt).scalars().first()
    
            if visitor and visitor.check_password(form.password.data):
                return jsonify({
                    "message": "Login successful",
                    "visitor_id": visitor.id,
                    "email_verified": visitor.is_email_verified,
                    "phone_verified": visitor.is_phone_verified,
                    "payment_done": visitor.is_payment_done,
                    "full_name": visitor.full_name
                }), 200
    
            return jsonify({"error": "Invalid email or password"}), 401
        return jsonify({"errors": form.errors}), 400
                    