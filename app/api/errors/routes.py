# ./app/api/errors/routes.py

from . import errors

@errors.app_errorhandler(404)
def error_404(error):
    return "404 page"
    
