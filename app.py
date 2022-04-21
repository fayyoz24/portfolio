from enum import unique
from sre_constants import SUCCESS
from flask import Flask, render_template, request, flash
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = "my app"

db = SQLAlchemy(app)

class Users(db.Model):
    user_id = db.Column(db.String(10), primary_key = True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=False)
    message = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable = False, default=db.func.now())

    def __init__(self,user_id, name, email, message):
        self.name=name
        self.email = email
        self.message = message
        self.user_id = user_id


@app.route('/', methods=['GET'])
def index():
    return render_template("base.html")

@app.route('/contact', methods=['POST'])
def indx():
    if request.method=='POST':
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("text")
        user_id = str(uuid.uuid4())
        
        user = Users(user_id=user_id, name=name, email=email, message=message)
        db.create_all(app=app)
        db.session.add(user) #Add user to the database
        db.session.commit() #Commit the changes to the database
        flash(f"Welcome {name}")
        return render_template('base.html', success=True)

    return render_template('base.html')


if __name__== "__main__":
    app.run(debug=True)

