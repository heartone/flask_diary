from flask import render_template, request, url_for, redirect, session, flash
from diary import app, login_check
from lib.db import db
from lib.models import User

# トップページを表示
@app.route('/')
@login_check
def top():
    user = User.query.get(session.get('auth_id'))
    return render_template('top.html', user=user)
    
# ログインページを表示
@app.route('/login')
def login():
    # ログイン済みかどうかをチェック
    if session.get('auth_id'):
        flash('すでにログインしています')
        return redirect(url_for('top'))
    
    # 未ログイン時のみ、ログインページを表示
    return render_template('login.html')

# ログイン処理
@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter(User.email == email).filter(User.password == password).first()
    if not user:
        flash('ログインできませんでした', 'danger')
        return redirect(url_for('login'))
    
    session['auth_id'] = user.id 

    flash('ログインしました', 'success')
    return redirect(url_for('top'))

#  ログアウト処理
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('auth_id', None)
    flash('ログアウトしました', 'success')
    return redirect(url_for('login'))
