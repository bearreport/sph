from flask import Flask, render_template, request, redirect, flash
from mailchimp3 import MailChimp
import hashlib
import os
from config import *


#create a flask instance
app = Flask(__name__)
app.config.from_pyfile('config.py')
#set a secret key
app.secret_key = ".+=;=\xe2'\x81\xbb\x94` `\xe1\xebf\xb9B9\x910\xd1\xf1\xc9"



#configure mailchimp
client = MailChimp('bearreport', MAILCHIMP_API_KEY) #username, API key


#default route leads to splashpage
@app.route('/')
def index():
    return render_template('splash.html')



#app routing for the mailchimp signup on the splash page
@app.route('/signup', methods = ['POST'])
def signup():
    signup = False
    email = request.form['email'] #pulls values from the form on the splash page
    fname = request.form['fname']
    lname = request.form['lname']
    school = request.form['school']
    schooldist = request.form['schooldist']
    city = request.form['city']
    state = request.form['state']
    print("Attempting to register email address:'" + email + "'") #this prints to the Python console, not the browser console
    try: #try to post to mailchimp - duplicate email causes HTTP error 400
        client.lists.members.create('2f961434b0', { #mailchimp list id
        'email_address': email,
        'status': 'subscribed',
         'merge_fields': {
            'FNAME': fname,
            'LNAME': lname,
            'SCHOOL': school,
            'SCHOOLDIST': schooldist,
            'CITY': city,
            'STATE': state
    },
    })
        print("Registration successful!")
        flash("Registration successful! Thanks for signing up to be part of schoolpinnd.")
    except:  #if the email already exists or is invalid, catch it here
        print("Error with e-mail acquistion")
        flash("There was a problem with registering your e-mail address! Check your email for confirmation if you already registered and make sure you are submitting a valid address.")
    return render_template('splash.html', signup=True)


#run flask app
if __name__ == '__main__':
    app.debug = True

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
