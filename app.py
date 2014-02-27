from flask import Flask, render_template, request, redirect, session, url_for, flash
import model

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

@app.route("/") # Default is GET request
def index():
    user_id = session.get("user_id")
    if session.get("user_id"):
        username = model.get_name_by_user(user_id)
        flash("Welcome %s" % username)
        return redirect(url_for("view_user",username=username ))
    else:
        return render_template("index.html")

@app.route("/", methods=["POST"])
def process_login():
    username = request.form.get("username")
    password = request.form.get("password")

    user_id = model.authenticate(username, password)

    if user_id != None:
        # flash("User authenticated!") 
        session['user_id'] = user_id
    else:
        flash("Password incorrect, there may be an issue.") 
    
    return redirect(url_for("index"))

@app.route("/register")
def register():
    user_id = session.get("user_id")
    if user_id:
        username = model.get_name_by_user(user_id)
        return redirect(url_for("view_user",username=username ))
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/user/<username>")
def view_user(username):
    check_logged_in = session.get("user_id")

    user_id = model.get_user_by_name(username)
    if user_id == None:
        flash("That user does not exist.")
        return redirect(url_for("register"))
    else: 
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

@app.route("/register", methods=["POST"])
def create_account():
    username= request.form.get("username")
    password= request.form.get("password")
    verify_password= request.form.get("password_verify")

    user_id = session.get("user_id")
    if user_id:
        username = model.get_name_by_user(user_id)
        return redirect(url_for("view_user",username=username )) 
    elif model.get_user_by_name(username) != None:
        flash("That username is taken, please try another")
        return redirect(url_for("register"))
    elif verify_password != password:
        flash("Your passwords didn't match")
        return redirect(url_for("register"))
    #check if password verify matches password
    else:
        model.make_new_user(username, password)
        flash("Your account has been created please login") 
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug = True)
