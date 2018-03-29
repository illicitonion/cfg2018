# Import the requests library so that we can use it to call the mailgun API.
import requests

# Import flask so that we can create a web application.
from flask import Flask, render_template, request

# YOU NEED TO CHANGE THIS!
# Fill in these variables with your own information:
mailgun_domain = "PUT_YOUR_MAILGUN_DOMAIN_HERE"
# Remember, don't put your API key on github :)
mailgun_api_key = "PUT_YOUR_MAILGUN_API_KEY_HERE"
your_email_address = "PUT_YOUR_EMAIL_ADDRESS_HERE"

# A function for sending email. Note that the name of the paramenter, "subject"
# is just how we can refer to the first parameter which the function was called with.
# Anyone who calls this function doesn't need to know it's called subject; they can
# use any variable names they want.
def send_simple_message(subject):
    # Use the requests library to call the mailgun API.
    return requests.post(
        "https://api.mailgun.net/v3/{}/messages".format(mailgun_domain),
        auth=("api", mailgun_api_key),
        # The dictionary of parameters to give to the mailgun API.
        data={
          "from": "Excited CFG Student <mailgun@{}>".format(mailgun_domain),
          "to": [your_email_address],
          "subject": subject,
          "text": "Testing some Mailgun awesomness!"
        }
    )

# Make our web application with Flask:
app = Flask("MyApp")

@app.route("/")
def hello():
    return "Hello World"

# If you visit /registration, show a form.
@app.route("/registration")
def registration():
    return render_template("registration.html")

# When a form with action=signup and method=post is submitted, run this code.
@app.route("/signup", methods=["POST"])
def handle_signup_form():
    # request.form is a dictionary where the keys are the same as the names of the <input> elements in the form and the values are the contents of those fields.
    form_data = request.form
    # registration.html had an <input> tag with name "name" so we can get its value from the dictionary.
    name_from_form = form_data["name"]

    # Make a subject for our email.
    subject_for_email = "{} wanted to send you an email".format(name_from_form)

    # Send an email!
    send_simple_message(subject_for_email)

    # And show some output in the web browser
    return "You've got email from {}!".format(name_from_form)

app.run(debug=True)
