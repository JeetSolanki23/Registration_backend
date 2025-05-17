# ./app/blueprints/__init__.py
#from .main import main as main_blueprint
from .auth import auth as auth_blueprint
from .errors import errors as errors_blueprint
 

def register_api(app):
    app.register_blueprint(auth_blueprint,url_prefix='/api/auth')
    app.register_blueprint(errors_blueprint)
    #app.register_blueprint(main_blueprint,url_prefix='/')
    



__all__ = ["auth_blueprint", "errors_blueprint",]
