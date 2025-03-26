from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# Configure SQLAlchemy database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SECRET_KEY'] = os.urandom(24).hex()

db = SQLAlchemy(app)

class tbl_user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)

    def __init__(self, username):
        self.username = username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Create database tables
with app.app_context():
    db.create_all()
    print('Database connected')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Username and password are required!", "error")
            return redirect(url_for("signup"))

        existing_user = tbl_user.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already taken!", "error")
            return redirect(url_for("signup"))

        try:
            new_user = tbl_user(username=username)
            new_user.set_password(password)
            
            db.session.add(new_user)
            db.session.commit()
                
            flash("Account created successfully!", "success")
            return redirect(url_for("home"))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Database error: {str(e)}")
            flash(f"Error creating account. Please try again. {str(e)}", "error")
            return redirect(url_for("signup"))
    
    return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True)
