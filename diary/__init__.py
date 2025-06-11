from flask import Flask, request, url_for, redirect, session, flash

app = Flask(__name__)
app.config.from_object('diary.config') 
app.config.from_object('lib.config')

from lib.db import init_db
init_db(app)

from functools import wraps

# ログインチェックデコレータの定義
def login_check(view):
    @wraps(view)
    def inner(*args, **kwargs):
        if not session.get('auth_id'):
            flash('まだログインしていません', 'danger')
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return inner

from diary.views import auth