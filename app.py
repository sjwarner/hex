from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
engine = create_engine('sqlite:///meetme.db', echo=True)

app = Flask(__name__)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('home.html')

@app.route('/login', methods=['POST'])
def do_admin_login():

    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        session['logged_in'] = True
        session['username'] = POST_USERNAME
    else:
        flash('wrong password!')
    return home()

@app.route('/registration')
def do_registration():
    return render_template('register.html')

@app.route('/event_page/<id>')
def get_event_page(id):

    Session = sessionmaker(bind=engine)
    s = Session()
    event = s.query(Event).filter(Event.id==id).one()
    val = s.query(exists().where(Attendee.username==session['username'] and Attendee.event_id==id))

    return render_template('event_page.html', event=event, already_participant=val)

@app.route('/join', methods=['POST'])
def do_join():

    attendee = Attendee(request.form['id'], session['username'])

    Session = sessionmaker(bind=engine)
    s = Session()
    s.add(attendee)
    s.commit()

    return home()

@app.route('/register', methods=['POST'])
def do_register():

    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()

    user = User(request.form['username'], request.form['password'])

    Session = sessionmaker(bind=engine)
    s = Session()
    s.add(user)
    s.commit()

    return home()

@app.route('/event_form')
def event_form():
    return render_template('create_event.html')

@app.route('/event_list')
def event_list():
    Session = sessionmaker(bind=engine)
    s = Session()
    events = s.query(Event).all()
    return render_template("event_list.html",
                           title="Events",
                           events=events)

@app.route('/create_event', methods=['POST'])
def do_create_event():

    event = Event(session['username'], request.form['event-name'],
            request.form['event-description'], request.form['event-location'],
            True)

    Session = sessionmaker(bind=engine)
    s = Session()
    s.add(event)
    s.commit()

    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    session['username'] = ''
    return home()

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
