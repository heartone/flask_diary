# DB接続設定
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{password}@{host}/{db}'.format(**{
    'user': 'postgres',
    'password': '',
    'host': 'localhost:5432',
    'db': 'flask_diary',
})
SQLALCHEMY_TRACK_MODIFICATIONS = False