# -*- coding: utf-8 -*-
from flask import render_template, jsonify
from app.forms import *
from app.models import *
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('all.html', tickets=db.session.query(ticket).all())

@app.route('/api/<method>')
def api(method):
    if method == "get_queue":
        tickets = db.session.query(ticket).all()
        data = []
        for i in tickets:
            if i.active and not(i.reception):
                data.append(i.id)
        return jsonify(data)
    if method == "get_queue_doctor":
        tickets = db.session.query(ticket).all()
        data = {}
        for i in tickets:
            if i.active and not (i.reception):
                data[i.id] = i.last_name
            tmp = []
            if i.active == i.reception == True:
                print(i.id)
                print(i.last_name)
                tmp.append(i.id)
                tmp.append(i.last_name)
                #if data.get('reception'):
                    #print("prikol")
                if str(tmp) != "[]" and not(data.get('reception')):
                    print(tmp)
                    data.update({'reception': tmp})
                #if not (data.get('reception')):
                    #data.update({'reception': tmp})
        return jsonify(data)

    return jsonify("Bad Request")

@app.route('/doctor', methods=['GET', 'POST'])
def doctor():
    print(db.session.query(ticket.active, ticket.reception, ticket.id).all())
    if queue().data['nextq'] and queue().data['stopq']:
        return "Произошла ошибка, попробуйте открыть страницу в новой вкладке"
    if queue().data['nextq']:
        print("nextq")
    if queue().data['stopq']:
        print("stopq")
    return render_template('doctor.html', tickets=db.session.query(ticket).all(), queue=queue())

@app.route('/get_equeue', methods=['GET', 'POST'])
def get_equeue():
    form = getTicet_F()
    if form.validate_on_submit():
        tickett = ticket(last_name=form.last_name.data)
        db.session.add(tickett)
        db.session.commit()
        # print(tickett.id) - айди тикета
        # print(tickett.last_name) - и фамилия чела собсна
    return render_template('add.html', form=form)

@app.errorhandler(404)
def not_found_error(error):
        return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0')