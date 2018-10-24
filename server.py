from flask import Flask, render_template, request, redirect, session, flash
import re
app = Flask(__name__)
app.secret_key = "superSecret"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
    if 'email' in session:
        session['email'] = session['email']
    else:
        session['email'] = "Enter email (ex. yourname@example.com)"
    if 'first_name' in session:
        session['first_name'] = session['first_name']
    else:
        session['first_name'] = "Enter First Name"
    if 'last_name' in session:
        session['last_name'] = session['last_name']
    else:
        session['last_name'] = "Enter Last Name"
    return render_template("index.html", email=session['email'], f_name=session['first_name'], l_name=session['last_name'])

@app.route('/register', methods=['POST'])
def register():
    count = 0
    upper = 0
    lower = 0
    # Check email #
    if len(request.form['email']) < 1:
        flash(u'Email is required!', 'error')
    elif not EMAIL_REGEX.match(request.form['email']):
        flash(u'Invalid email!', 'error')
    else:
        count += 1
        session['email'] = request.form['email']
    # Check first name#
    if len(request.form['first_name']) < 1:
        flash(u'First Name is required!', 'error')
    elif str.isalpha(request.form['first_name']) == False:
        flash(u'First Name must contain only alphanumeric characters!', 'error')
    else:
        count += 1
        session['first_name'] = request.form['first_name']
    # Check last name #
    if len(request.form['last_name']) < 1:
        flash(u'Last Name is required!', 'error')
    elif str.isalpha(request.form['last_name']) == False:
        flash(u'Last Name must contain only alphanumeric characters!', 'error')
    else:
        count += 1
        session['last_name'] = request.form['last_name']
    # check password #
    if len(request.form['password']) < 1:
        flash(u'Password is required!', 'error')
    elif len(request.form['password']) >= 1 and len(request.form['password']) < 8:
        flash(u'Password must be longer thant 8 characters!', 'error')
    else:
        count += 1
    # verify password has one upper and lower case letter #
    for x in request.form['password']:
        if str.islower(x) == True:
            lower+=1
        if str.isupper(x) == True:
            upper+=1
    print(upper,lower)
    if lower > 0 and upper > 0:
        count+=1
    else:
        flash(u'Password must both an upper case and lower case character!', 'error')
    # verify password #
    if request.form['password_confirm'] != request.form['password']:
        flash(u'Your password confirmation must match your password!', 'error')
    else:
        count += 1
        session['password_confirm'] = request.form['password_confirm']
    if count == 6:
        flash(u'Thanks for submitting your information.','succes')
        session['password'] = request.form['password']
    return redirect('/')

@app.route('/clear')
def clear():
    session.clear()
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)

