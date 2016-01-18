import os
import glob
from flask import request, session, g, redirect, url_for, abort, render_template, flash
from app import app
from .connection import db, customers
path = "C:\\Users\\POLY\Google Drive\\Desktop\\business\\app\\test\\*"

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = request.form['inputEmail']
        password =request.form['inputPassword']
        print user
        print "*******************************"
        users = customers.find_one({'email': user})
        if users != None:
            print users.get("email")
            print users.get("password")
            print "*******************************" 
            if user != users.get("email"):
                error = 'Invalid username'
            elif password != users.get("password"):
                error = 'Invalid password'
            else:
                session['user'] = users.get("email") 
                session['userId'] = str(users.get("_id"))
                session['userSector'] = str(users.get("sector"))
                flash('You are logged in')
                return redirect(url_for('about_signedIn'))
        elif users == None:
            error = 'User not found'
            return redirect(url_for('signup'))      
    return render_template('signIn.html', error=error)

@app.route('/logout')
def logout():
    files = glob.glob(path)
    for f in files:
        os.remove(f)
    if session.pop(session['user'], None):
        flash('You were logged out')
    return redirect(url_for('home'))

"""if __name__ == '__main__':
	app.debug = True
	app.run()"""
