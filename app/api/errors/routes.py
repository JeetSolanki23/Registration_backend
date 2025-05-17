# ./app/api/errors/routes.py
from flask import jsonify
from . import errors
from werkzeug.http import HTTP_STATUS_CODES

@errors.app_errorhandler(404)
def handle_not_found_error(e):
    return jsonify({
        'message': HTTP_STATUS_CODES.get(404, 'Unknown error'),
        'code': 404
    }), 404

@errors.app_errorhandler(405)
def handle_method_not_allowed(e):
    return jsonify({
        'message': HTTP_STATUS_CODES.get(405, 'Unknown error'),
        'code': 405
    }), 405

@errors.app_errorhandler(500)
def handle_internal_server_error(e):
    return jsonify({
        'message': 'Internal server error',
        'code': 500
    }), 500
