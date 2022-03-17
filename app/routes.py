# -*- coding: utf-8 -*-
from flask import render_template, jsonify
from app.forms import *
from app.models import *
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('all.html', tickets=db.session.query(ticket).all())

@app.route('/api/get_queue')
def get_queue():
    tickets = db.session.query(ticket).all()
    data = []
    for i in tickets:
        data.append(i.id)
    print(data)
    return jsonify(data)

@app.route('/doctor')
def doctor():
    return render_template('doctor.html', tickets=db.session.query(ticket).all())

@app.route('/get_equeue', methods=['GET', 'POST'])
def get_equeue():
    form = getTicet_F()
    if form.validate_on_submit():
        tickett = ticket(last_name=form.last_name.data)
        db.session.add(tickett)
        db.session.commit()
        # print(tickett.id)
        # print(tickett.last_name)
    return render_template('add.html', form=form)

#@app.route('/favicon')
#@app.route('/favicon.ico')
#def favicon():
#    return send_from_directory('static/', 'image/favicons/favicon.ico')

@app.errorhandler(404)
def not_found_error(error):
        return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0')