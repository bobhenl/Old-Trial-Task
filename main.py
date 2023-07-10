from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash
from datetime import datetime
import sqlite3


app = Flask(__name__)
password_hash_type = "sha256"


@app.route("/register", methods=["POST", "GET"])
def regiser():
    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")
        password_repeat = request.form.get("password_repeat")


        if password != password_repeat:
            return render_template("register.html", error_msg="Password do not match")
        
        with sqlite3.connect("data.db") as conn:
            already_exist = conn.cursor().execute("SELECT * FROM accounts WHERE email=?", (email,)).fetchall()


        if len(already_exist) == 0:
            password_hash = generate_password_hash(password, password_hash_type)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            with sqlite3.connect("data.db") as conn:
                conn.cursor().execute("INSERT INTO accounts(date_created, email, password) VALUES(?, ?, ?)", (timestamp, email, password_hash,))
                conn.commit()
            return "Your account has been created"

        else:
            return render_template("register.html", error_msg="This email is already registered")
    else:
        return render_template("register.html")


@app.route("/accounts")
def accounts():
    with sqlite3.connect("data.db") as conn:
        data = conn.cursor().execute("SELECT * FROM accounts").fetchall()
    
    return render_template("accounts.html", accounts=data)



if __name__ == "__main__":
    app.run(debug=True, port=3000)