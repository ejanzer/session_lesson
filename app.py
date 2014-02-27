from flask import Flask, render_template, request, redirect, session, url_for, flash
import model

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

# handler for /
@app.route("/") 
def index():
    """Handler for /. Redirects to login page if not logged in."""
    user_id = session.get("user_id")
    if session.get("user_id"):
        username = model.get_name_by_user(user_id)
        flash("Welcome %s" % username)
        return redirect(url_for("view_user",username=username ))
    else:
    #otherwise send user to login page    
        return render_template("index.html")

# handler for login form
@app.route("/", methods=["POST"])
def process_login():
    username = request.form.get("username")
    password = request.form.get("password")

    # authenticate user. if authenticated, returns id. else, returns None
    user_id = model.authenticate(username, password)

    if user_id != None:
        # if user authenticated, set the user_id on the session
        session['user_id'] = user_id
    else:
        # if not authenticated, flash an error message
        flash("Password or username incorrect. Please try again.") 
    
    # everyone redirects to index. if auth, this will redirect again to wall. 
    # this seems unnecessary - should we just put it in the if/else?  
    return redirect(url_for("index"))

# handler for /register (from login page)
@app.route("/register")
def register():
    # if user is logged in, redirect to their wall
    # otherwise, else send to register.html
    user_id = session.get("user_id")
    if user_id:
        username = model.get_name_by_user(user_id)
        return redirect(url_for("view_user",username=username ))
    else:   
        return render_template("register.html")

# TODO: add logout link in template
@app.route("/logout")
def logout():
    # clear session and redirect to login
    session.clear()
    return redirect(url_for("index"))

# handler for viewing a user's wall
@app.route("/user/<username>")
def view_user(username):
    # TODO: How do you navigate to other users' walls?
    # TODO: Sort & display by datetime

    # check if the user is logged in. 
    # the template uses this to determine whether or not to display wall post form
    check_logged_in = session.get("user_id")

    # get user_id for the owner of the page
    user_id = model.get_user_by_name(username)
    if user_id == None:
        flash("That user does not exist.")
        # Is this where we should redirect to?
        return redirect(url_for("register"))
    else: 
        # get list of wall_posts from database
        # wall_posts is a list of tuples
        wall_posts = model.get_wall_by_user(user_id)

        html = render_template("wall.html", wall_posts=wall_posts, check_logged_in=check_logged_in, username=username)
        return html

# handler for posting on a user's wall
@app.route("/user/<username>", methods=["POST"])
def post_to_wall(username):
    # TODO: Add datetime

    #request.form is dictionary from form with method post 
    # get content from submitted form
    content = request.form.get("content")

    #get the id of the current user from the session
    author_id = session.get("user_id")

    # look up the owner of the page
    owner_id = model.get_user_by_name(username)

    # add post to database
    model.post_to_wall(owner_id, author_id, content)

    # send user back to same page
    # url_for is a flask function that finds the right url based on handler name
    return redirect(url_for("view_user",username=username ))

# handler for when a user creates a new account (form method set to POST)
@app.route("/register", methods=["POST"])
def create_account():

    # get username, password and verify_password from form data
    username = request.form.get("username")
    password = request.form.get("password")
    verify_password = request.form.get("password_verify")

    # get user id from session, if it exists
    user_id = session.get("user_id")
    if user_id:
        # if the user is logged in, send them to their own wall
        username = model.get_name_by_user(user_id)
        return redirect(url_for("view_user",username=username)) 

    # if username is already in the database, flash error message and redirect to same page
    elif model.get_user_by_name(username) != None:
        flash("That username is taken, please try another")
        return redirect(url_for("register"))

    # if the passwords don't match, flash error message and redirect
    elif verify_password != password:
        flash("Your passwords didn't match")
        return redirect(url_for("register"))

    #check if password verify matches password
    else:
        # if they passed all those checks, create a new user in the database
        # and redirect to their own page
        model.make_new_user(username, password)

        # flashed messages are fetched using flask function in the jinja template
        # in HTML, call get_flashed_messages() to display
        flash("Your account has been created please login") 
        return redirect(url_for("index"))

# only run the server if this is main (not if imported)
# set debug to false for production!
if __name__ == "__main__":
    app.run(debug = True)
