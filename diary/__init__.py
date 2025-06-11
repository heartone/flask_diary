from flask import Flask

app = Flask(__name__)
app.config.from_object('diary.config') 
app.config.from_object('lib.config')

from lib.db import init_db
init_db(app)
