# SQLAlchemyをインポート
from flask_sqlalchemy import SQLAlchemy 
# Migrateクラスをインポート
from flask_migrate import Migrate 

# SQLAlchemyをインスタンス化
db = SQLAlchemy() 

# modelsパッケージをインポート（dbが定義された後で記述）
import lib.models 

def init_db(app):
    db.init_app(app) 
    Migrate(app, db)