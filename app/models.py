from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
import random

class ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(64))
    active = db.Column(db.Boolean, default=True)
    reception = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Ticket {}>'.format(self.id)

    def repr(self):
        return ''.format(self.id)

@login.user_loader
def load_user(id):
    return ticket.query.get(int(id))