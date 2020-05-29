"""Starts app."""
from flask import render_template
from app import create_app

server = create_app()


@server.errorhandler(404)
def page_not_found(error):
    """404 page."""
    # note that we set the 404 status explicitly
    return render_template("404.html"), 404
