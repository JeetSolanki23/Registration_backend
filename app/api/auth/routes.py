# ./app/api/auth/routes.py
from flask import jsonify, request
from . import auth
from .forms import VisitorRegistrationForm, VisitorLoginForm
from app.services import AuthService

@auth.route('/register', methods=['GET', 'POST'])
def ragistor():
    form = VisitorRegistrationForm(data=request.json)
    
    if form.validate():
        r = AuthService.ragistor(form)
        return r
        
        
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = VisitorLoginForm(meta={'csrf': False})
    
    if form.validate():
        r = AuthService.login(form)
        return r