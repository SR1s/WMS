from flask import Blueprint, render_template, abort

accounts = Blueprint("accounts",__name__)

@accounts.route("/login")
def login():
	return "login form will show here"

@accounts.route("/login", methods=['POST',])
def perform_login():
	return "you have log in!"