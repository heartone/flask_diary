from flask import render_template, request, url_for, redirect, session, flash, Blueprint
from sqlalchemy import or_
from diary import app, login_check
from lib.db import db
from lib.models import Diary
from datetime import datetime 

diary = Blueprint('diary', __name__)

# 日記一覧画面
@diary.route('/')
@login_check
def index():
    # リクエストパラメータ
    keyword = request.args.get('keyword')
    page = request.args.get('page', default=1, type=int)

    # 日記クエリ
    query = Diary.query.order_by(Diary.created_at.desc())

    # 自分の日記のみ取得
    query = query.filter(Diary.user_id == session.get('auth_id'))

    # キーワード検索
    if keyword:
        word = f'%{keyword}%'
        query = query.filter(or_(Diary.title.like(word), Diary.content.like(word)))

    diaries = query.paginate(page=page, per_page=10)
    return render_template('diaries/index.html', diaries=diaries)
    
# 日記詳細画面
@diary.route('/<int:id>')
@login_check 
def show(id):
    diary = Diary.query.get(id)

    # 認可チェック
    if not diary or diary.user_id != session.get('auth_id'):
        flash('不正なアクセスです', 'danger')
        return redirect(url_for('diary.index'))

    return render_template('diaries/show.html', diary=diary)

# 日記投稿画面
@diary.route('/new')
@login_check 
def new():
    diary = Diary()
    return render_template('diaries/new.html', diary=diary)

# 日記登録処理
@diary.route('/create', methods=['POST'])
@login_check 
def create():
    # リクエストパラメータ
    title = request.form.get('title') or ''
    content = request.form.get('content') or ''

    # バリデーション（本当はモデルでやりたいが便宜上ここで）
    errors = []

    # タイトルは必須（空文字が入ってしまわないように）
    if not title:
        errors.append('タイトルを入力してください')
    
    # 本文は必須（空文字が入ってしまわないように）
    if not content:
        errors.append('本文を入力してください')
    
    # エラーがあったらフラッシュメッセージ＆リダイレクト
    if errors:
        for e in errors:
            flash(e, 'danger')
        return redirect(url_for('diary.new'))
    
    diary = Diary(
        user_id = session.get('auth_id'),
        title = title, 
        content = content, 
        created_at = datetime.now()
    )
    
    try:
        db.session.add(diary)
        db.session.commit()
    except Exception as e:
        print(e)
        flash('投稿できませんでした', 'danger')
        return redirect(url_for('diary.new'))
    
    flash('投稿しました', 'success')
    return redirect(url_for('diary.show', id=diary.id))

# 日記編集画面
@diary.route('/<int:id>/edit')
@login_check 
def edit(id):
    diary = Diary.query.get(id)

    # 認可チェック
    if not diary or diary.user_id != session.get('auth_id'):
        flash('不正なアクセスです', 'danger')
        return redirect(url_for('diary.index'))

    return render_template('diaries/edit.html', diary=diary)

# 日記更新処理
@diary.route('/<int:id>/update', methods=['POST'])
@login_check 
def update(id):
    diary = Diary.query.get(id)

    # 認可チェック
    if not diary or diary.user_id != session.get('auth_id'):
        flash('不正なアクセスです', 'danger')
        return redirect(url_for('diary.index'))
    
    # リクエストパラメータ
    title = request.form.get('title') or ''
    content = request.form.get('content') or ''

    errors = []
    
    if not title:
        errors.append('タイトルを入力してください')
    
    if not content: 
        errors.append('本文を入力してください')
    
    if errors:
        for e in errors:
            flash(e, 'dangeR')
        return redirect(url_for('diary.edit', id=id))

    diary.title = title 
    diary.content = content

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        flash('更新できませんでした', 'danger')
        return redirect(url_for('diary.edit', id=id))
    
    flash('日記を更新しました', 'success')
    return redirect(url_for('diary.show', id=id))

# 日記削除処理
@diary.route('/<int:id>/delete', methods=['POST'])
@login_check 
def delete(id):
    diary = Diary.query.get(id)

    # 認可チェック
    if not diary or diary.user_id != session.get('auth_id'):
        flash('不正なアクセスです', 'danger')
        return redirect(url_for('diary.index'))
    
    db.session.delete(diary)
    db.session.commit()

    flash('削除しました', 'success')
    return redirect(url_for('diary.index'))
