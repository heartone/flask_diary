from lib.db import db 

class Diary(db.Model):
    __tablename__ = 'diaries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    title = db.Column(db.String(50), nullable=True)
    content = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship('User', uselist=False)