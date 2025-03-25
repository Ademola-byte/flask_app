from flask import Flask, render_template, request, redirect, flash, url_for;
# from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)





@app.route("/")
def home():
    return render_template("index.html")





@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        return redirect(url_for("index.html"))
    

    else:
        return render_template("signup.html") 

if __name__ == "__main__":
    app.run(debug=True)