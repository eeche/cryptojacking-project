from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.models import Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db:5432/blog'
db = SQLAlchemy(app)

from app import routes, models

@app.before_first_request
def create_tables():
    db.create_all()
