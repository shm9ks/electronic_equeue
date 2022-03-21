# -*- coding: utf-8 -*-
from flask import render_template, flash
from flask_json import as_json
from app.forms import *
from app.models import *
from app import app
import json


@app.route('/')
@app.route('/index')
def index():
    return render_template('all.html', tickets=db.session.query(ticket).all())


@app.route('/api/<method>/<mean>')
@as_json
def api(method, mean):
    if method == "get":
        data = {}
        if mean == "queue":
            tickets = db.session.query(ticket).all()
            for i in tickets:
                if i.active and not i.reception:
                    data[str(i.id)] = False
                if i.active == i.reception == True:
                    data[str(i.id)] = True
            return data

        if mean == "queue_doctor":
            tickets = db.session.query(ticket).all()
            for i in tickets:
                if i.active and not i.reception:
                    data[str(i.id)] = i.last_name
                tmp = []
                if i.active == i.reception == True:
                    tmp.append(i.id)
                    tmp.append(i.last_name)
                    if str(tmp) != "[]" and not (data.get('reception')):
                        data.update({'reception': tmp})
            return data
    return "error"


@app.route('/doctor', methods=['GET', 'POST'])
def doctor():
    #print(db.session.query(ticket.active, ticket.reception, ticket.id).all())
    if queue().data['nextq'] and queue().data['stopq']:
        flash("Произошла ошибка, попробуйте открыть страницу в новой вкладке")
    if queue().data['nextq']:
        queue_doc = json.loads(api(method="get", mean="queue_doctor").data.decode('utf-8'))
        if queue_doc.get('reception'):
            tick = db.session.query(ticket).filter(ticket.id == (queue_doc['reception'][0])).all()[0]
            tick.active = False
            tick.reception = False
            db.session.commit()
            try:
                tick = db.session.query(ticket).filter(ticket.id == (queue_doc['reception'][0]+1)).all()[0]
                tick.reception = True
                db.session.commit()
                queue_doc = json.loads(api(method="get", mean="queue_doctor").data.decode('utf-8'))
                flash(f"Следующий пациент - ID тикета - {queue_doc['reception'][0]}, фамилия {queue_doc['reception'][1]}")
            except:
                flash("Не удалось найти пациента в очереди")
        else:
            flash_str = ''
            try:
                if list(queue_doc.keys())[0].isdigit():
                    tick = db.session.query(ticket).filter(ticket.id == (list(queue_doc.keys())[0])).all()[0]
                    tick.active = True
                    tick.reception = True
                    db.session.commit()
            except:
                flash_str = "Ошибка очереди, возможна она пуста"
            if flash_str == '':
                queue_doc = json.loads(api(method="get", mean="queue_doctor").data.decode('utf-8'))
                flash_str = f"Следующий пациент - ID тикета - {queue_doc['reception'][0]}, фамилия {queue_doc['reception'][1]}"
            flash(flash_str)

    if queue().data['stopq']:
        queue_doc = json.loads(api(method="get", mean="queue_doctor").data.decode('utf-8'))
        if queue_doc.get('reception'):
            tick = db.session.query(ticket).filter(ticket.id == (queue_doc['reception'][0])).all()[0]
            tick.active = False
            tick.reception = False
            db.session.commit()
        flash('Вы остановили прием пациентов')
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
