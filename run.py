from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from app import app, db

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
