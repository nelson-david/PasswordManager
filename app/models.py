from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(), nullable=False)
	email = db.Column(db.String(), nullable=False)
	password = db.Column(db.String(), nullable=False)
	date_joined = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

	saved_password = db.relationship("Password", backref="author", lazy=True)

	def __repr__(self):
		return f"{self.name}, {self.email}, {self.date_joined} "

class Password(db.Model):
	id = db.Column(db.Integer, primary_key=True, nullable=False)
	allies = db.Column(db.String(), nullable=False)
	fake_password = db.Column(db.String(), nullable=False)
	original_password = db.Column(db.String(), nullable=False)
	date_added = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"{self.allies}, {self.password}, {self.original} "