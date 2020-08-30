from app import app, db, bcrypt
from app.models import User, Password
from flask import render_template, jsonify, request, url_for, redirect, flash
from flask_login import login_user, current_user, logout_user

import secrets

@app.route("/")
def home():
	if current_user.is_authenticated:
		return redirect(url_for('main'))
	return render_template("index.html")

@app.route("/get_started")
def get_started():
	if current_user.is_authenticated:
		return redirect(url_for('main'))
	return render_template("get_started.html")

@app.route("/add_user", methods=['POST'])
def add_user():
	check_user = User.query.filter_by(email=request.form['email']).first()
	if check_user:
		return jsonify({'returns':'already_exist'})
	else:
		hash_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
		new_user = User(name=request.form['name'], email=request.form['email'],\
			password=hash_password)
		db.session.add(new_user)
		db.session.commit()
		return jsonify({'returns':'success'})


@app.route("/validate_user", methods=['POST'])
def validate_user():
	user = User.query.filter_by(email=request.form['email']).first()
	if user and bcrypt.check_password_hash(user.password, request.form['password']):
		login_user(user, remember=True)
		return jsonify({'returns':'logged_in'})
	else:
		return jsonify({'returns':'not_found'})


@app.route("/logout")
def logout():
	logout_user()
	flash("Logout successfull")
	return redirect(url_for('get_started'))



@app.route("/dashboard")
def main():
	if current_user.is_authenticated:
		return render_template("dashboard.html")
	return redirect(url_for('get_started'))

@app.route("/passwords")
def all_passwords():
	if current_user.is_authenticated:
		user_passwords = Password.query.filter_by(author=current_user).all()
		return render_template("all_password.html", user_passwords=user_passwords)
	return redirect(url_for('get_started'))

@app.route("/add_password", methods=['POST'])
def add_password():
	hash_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
	new_password = Password(allies=request.form['allies'].lower(), fake_password=hash_password,\
			original_password=request.form['password'], author=current_user)
	db.session.add(new_password)
	db.session.commit()
	return jsonify({'returns':'success'})

@app.route("/generate_password", methods=['POST'])
def generate_password():
	allies = request.form['allies']
	check_allies = Password.query.filter_by(allies=allies.lower()).first()
	if check_allies:
		return jsonify({'result':'exists'})
	new_password = secrets.token_hex(4)
	return jsonify({'result':new_password, 'allies':allies})

@app.route("/delete_password", methods=['POST'])
def delete_password():
	password = Password.query.get_or_404(request.form['id'])
	db.session.delete(password)
	db.session.commit()
	return jsonify({'returns':'success'})