from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from ..main import main
        
@main.route('/')
def hello():
    return render_template("welcome.html")

@main.route('/about')
def about():
    return "this is about page"
