# ./app/api/main/routes.py
from flask import redirect, url_for, flash, request
from . import main

@main.route('/')
def index():
    return "main route"
    