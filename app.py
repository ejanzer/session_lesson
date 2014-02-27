from flask import Flask, render_template, request, redirect, session, url_for, flash
import model

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

#when user first arrives at site login page
@app.route("/") # Default is GET request
def index():
    user_id = session.get("user_id")
    #check if the user is already logged in if so send them to their page
    if session.get("user_id"):
        username = model.get_name_by_user(user_id)
        flash("Welcome %s" % username)
        return redirect(url_for("view_user",username=username ))
    else:
    #otherwise send user to login page    
        return render_template("index.html")
#this handler gets activated when user uses log in form which is set to method: post
@app.route("/", methods=["POST"])
#once login submitted get from the form submission the username and password
def process_login():
    username = request.form.get("username")
    password = request.form.get("password")
    #and use the authenticate function to check if username and password match
    user_id = model.authenticate(username, password)

    if user_id != None:
        # flash("User authenticated!") 
        #setting the session user id to the user's user_id 
        session['user_id'] = user_id
    else:
        #if password entered incorrectly also if username doesn't exist
        flash("Password or username incorrect, there may be an issue.") 
    #send them back to login if there is an issue here
    #we are redirecting them either way here but it checks again if they are logged in    
    return redirect(url_for("index"))
#when user clicks on register from login page
@app.route("/register")
def register():
    #this get the user_id from session if it exists
    user_id = session.get("user_id")
    if user_id:
        #if you are logged in it redirects your to your own page
        username = model.get_name_by_user(user_id)
        return redirect(url_for("view_user",username=username ))
    else:   
    #if user is not logged it sends you to register page 
        return render_template("register.html")
#we don't yet have a logout button, but if logout in url session gets erased
@app.route("/logout")
def logout():
    session.clear()
    #and user gets redirected to login page
    return redirect(url_for("index"))
#view a specific users page, user gets sent here to their own page after logging in
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
        #this generates the wall page from template these variable are for jinja to include{{}}
        html = render_template("mypage.html", wall_posts=wall_posts, check_logged_in=check_logged_in, username=username)
        return html

#this get's activated when user is on someone's wall and they submit post
@app.route("/user/<username>", methods=["POST"])
def post_to_wall(username):
    #request.form is dictionary from form with method post 
    # get content from submitted form
    content = request.form.get("content")

    #get the current user from the session
    author_id = session.get("user_id")

    # look up the person whose page it is
    owner_id = model.get_user_by_name(username)

    # add post to database
    model.post_to_wall(owner_id, author_id, content)

    # send user back to same page
    # url_for is a flask function that finds the right url based on handler name
    return redirect(url_for("view_user",username=username ))

# handler for when a user creates a new account on the register page (form method set to POST)
@app.route("/register", methods=["POST"])
def create_account():

    # get username and password and verify_password from form data
    username= request.form.get("username")
    password= request.form.get("password")
    verify_password= request.form.get("password_verify")

    # get user id from session, if it exists
    user_id = session.get("user_id")
    if user_id:
        # if the user is logged in, send them to their own page
        username = model.get_name_by_user(user_id)
        return redirect(url_for("view_user",username=username )) 
    elif model.get_user_by_name(username) != None:
        # if username is already in the database, flash error message and redirect to same page
        flash("That username is taken, please try another")
        return redirect(url_for("register"))
    elif verify_password != password:
        # if the passwords don't match, flash error message and redirect
        flash("Your passwords didn't match")
        return redirect(url_for("register"))
    #check if password verify matches password
    else:
        # if they passed all those checks, create a new user in the database
        # and redirect to their own page
        model.make_new_user(username, password)
        # flashed messages are fetched using flask function in the jinja template
        # in HTML call get_flashed_messages() to display
        flash("Your account has been created please login") 
        return redirect(url_for("index"))

# only run the server if this is main (not if imported)
# set debug to false for production!
if __name__ == "__main__":
    app.run(debug = True)
