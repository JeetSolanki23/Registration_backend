from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

class APIError(Exception):
    """Base error class for API exceptions"""
    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code or 400
        self.payload = payload
    
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['code'] = self.status_code
        return rv

def register_error_handlers(app):
    """Register error handlers for the application"""
    
    @app.errorhandler(APIError)
    def handle_api_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    
    @app.errorhandler(404)
    def handle_not_found_error(e):
        return jsonify({
            'message': HTTP_STATUS_CODES.get(404, 'Unknown error'),
            'code': 404
        }), 404
    
    @app.errorhandler(405)
    def handle_method_not_allowed(e):
        return jsonify({
            'message': HTTP_STATUS_CODES.get(405, 'Unknown error'),
            'code': 405
        }), 405
    
    @app.errorhandler(500)
    def handle_internal_server_error(e):
        return jsonify({
            'message': 'Internal server error',
            'code': 500
        }), 500