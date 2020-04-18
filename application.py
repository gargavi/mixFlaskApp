

from flask import Flask, redirect, request, render_template, session, url_for, flash, get_flashed_messages


application = Flask(__name__)

@application.route("/")
def index(): 
    return "Hello World"

