import os
from flask import Blueprint, request, make_response
from app.models import User, Requests
from app.app import app_config

app = Blueprint('auth', __name__)



app.add_routes(app.UserRegistration, '/api/v1/auth/signup/')
app.add_routes(app.UserLogin, '/api/v1/auth/signin/')
api.add_routes(app.UserLogoutAccess, '/api/v1/auth/signout/')
api.add_routes(app.UserCreateRequest, '/api/v1/auth/requests/')
api.add_routes(app.UserGetSingleRequest, '/api/v1/requests/<request_id>/')
api.add_routes(app.UserGetAllRequests, '/api/v1/requests/')
api.add_routes(app.UserModifyRequest, '/api/v1/requests/<request_id>')
api.add_routes(app.UserDeleteRequest, '/api/v1/requests/<request_id>')
