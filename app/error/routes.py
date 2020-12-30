from flask import render_template, url_for 
from app import app 


@app.errorhandler(403)
def forbidden(error):
    return render_template('error/403.html'), 403

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'), 404

@app.errorhandler(500)
def internal_server_problem(error):
    return render_template('error/500.html'), 500

