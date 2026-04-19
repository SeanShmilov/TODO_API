from flask import Flask, jsonify, request, Blueprint
from werkzeug.exceptions import NotFound, BadRequest, Conflict, HTTPException

errors_bp = Blueprint("errors", __name__)

@errors_bp.app_errorhandler(HTTPException)
def handle_http_exception(e):
    # Formats error message as "404 Not Found: description"
    return jsonify({"ERROR": f"{e.code} {e.name}: {e.description}"}), e.code

@errors_bp.app_errorhandler(Exception)
def handle_unexpected_error(e):
    print(f"Unexpected Error: {e}") 
    
    response = {
        "error": "Internal Server Error",
        "message": "Something went wrong on our end"
    }
    return jsonify(response), 500