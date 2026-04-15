from flask import Flask, jsonify, request, Blueprint
from werkzeug.exceptions import NotFound, BadRequest, Conflict, HTTPException

errors_bp = Blueprint("errors", __name__)

@errors_bp.errorhandler(HTTPException)
def handle_http_exception(e):
    response = {
        "error": e.name,          
        "message": e.description   
    }
    return jsonify(response), e.code

@errors_bp.errorhandler(Exception)
def handle_unexpected_error(e):
    print(f"Unexpected Error: {e}") 
    
    response = {
        "error": "Internal Server Error",
        "message": "Something went wrong on our end"
    }
    return jsonify(response), 500