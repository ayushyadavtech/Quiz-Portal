from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Create Flask app
app = Flask(__name__)

# Secret key for sessions
app.config['SECRET_KEY'] = 'quizapp123secretkey'

# Database file location
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'

# Create database object
db = SQLAlchemy(app)

# Create login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from routes import *

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True , host = '0.0.0.0')     #app.run(debug=True, host='0.0.0.0')