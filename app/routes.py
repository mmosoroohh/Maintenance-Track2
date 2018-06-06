import os
from flask import Blueprint, request, make_response
from app.models import User, Requests

app = Blueprint('auth', __name__)

