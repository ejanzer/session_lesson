from flask import Flask, render_template, request, redirect, session, url_for, flash
import model

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

@app.route("/") # Default is GET request
def index():
    if session.get("user_id"):
        return "User %s is logged in!" % session['user_id']
    else:
        return render_template("index.html")

@app.route("/", methods=["POST"])
def process_login():
    username = request.form.get("username")
    password = request.form.get("password")

    user_id = model.authenticate(username, password)

    if user_id != None:
        flash("User authenticated!") 
        session['user_id'] = user_id
    else:
        flash("Password incorrect, there may be an issue.") 
    
    return redirect(url_for("index"))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/user/<username>")
def view_user(username):
    check_logged_in = session.get("user_id")

    user_id = model.get_user_by_name(username)
    #wall_posts is a list of tuples
    wall_posts = model.get_wall_by_user(user_id)
    html = render_template("mypage.html", wall_posts=wall_posts, check_logged_in=check_logged_in, username=username)
    return html

@app.route("/user/<username>", methods=["POST"])
def post_to_wall(username):
    #request.form is dictionary from form with method post 
    content = request.form.get("content")
    author_id = session.get("user_id")
    owner_id = model.get_user_by_name(username)
    model.post_to_wall(owner_id, author_id, content)
    return redirect(url_for("view_user",username=username ))


if __name__ == "__main__":
    app.run(debug = True)
