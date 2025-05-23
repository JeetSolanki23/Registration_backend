# ./app/blueprints/__init__.py
#from .main import main as main_blueprint
from .auth_route import auth as auth_blueprint
#from .errors import errors as errors_blueprint
from .otp_route import otp as otp_blueprint
from .payment_route import payment as payment_blueprint

def register_api(app):
    app.register_blueprint(auth_blueprint,url_prefix='/api/auth')
    #app.register_blueprint(errors_blueprint)
    app.register_blueprint(otp_blueprint,url_prefix='/api/otp')
    app.register_blueprint(payment_blueprint,url_prefix='/api/payment')
    



__all__ = ["auth_blueprint", "otp_blueprint", "errors_blueprint",]
